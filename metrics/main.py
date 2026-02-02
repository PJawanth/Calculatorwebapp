"""Metrics collection module using GitHub REST API."""

import json
import os
from datetime import UTC, datetime, timedelta
from typing import Any

import requests


class GitHubMetricsCollector:
    """Collects DevOps metrics from GitHub API."""

    def __init__(self) -> None:
        self.token = os.environ.get("GITHUB_TOKEN", "")
        self.repo = os.environ.get("GITHUB_REPOSITORY", "")
        self.window_days = int(os.environ.get("METRICS_WINDOW_DAYS", "30"))
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def _get(self, endpoint: str, params: dict[str, Any] | None = None) -> Any:
        """Make GET request to GitHub API."""
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    def _get_paginated(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> list[Any]:
        """Fetch all pages from a paginated endpoint."""
        params = params or {}
        params["per_page"] = 100
        params["page"] = 1
        all_items: list[Any] = []

        while True:
            items = self._get(endpoint, params)
            if not items:
                break
            all_items.extend(items)
            if len(items) < 100:
                break
            params["page"] += 1
            if params["page"] > 10:  # Safety limit
                break

        return all_items

    def _get_window_start(self) -> datetime:
        """Get the start of the metrics window."""
        return datetime.now(UTC) - timedelta(days=self.window_days)

    def _parse_datetime(self, dt_str: str) -> datetime:
        """Parse GitHub datetime string."""
        return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))

    def get_workflow_runs(self, workflow_name: str) -> list[dict[str, Any]]:
        """Get workflow runs for a specific workflow."""
        endpoint = f"/repos/{self.repo}/actions/runs"
        params = {"created": f">={self._get_window_start().strftime('%Y-%m-%d')}"}
        all_runs = self._get_paginated(endpoint, params)
        return [
            run
            for run in all_runs
            if run.get("name", "").lower() == workflow_name.lower()
        ]

    def collect_dora_metrics(self) -> dict[str, Any]:
        """Collect DORA metrics from CD workflow runs."""
        cd_runs = self.get_workflow_runs("CD - Azure Web App")

        total = len(cd_runs)
        successful = sum(1 for r in cd_runs if r["conclusion"] == "success")
        failed = sum(1 for r in cd_runs if r["conclusion"] == "failure")
        change_failure_rate = (failed / total * 100) if total > 0 else 0

        # MTTR proxy: time between first failed deploy and next successful deploy
        mttr_hours = None
        sorted_runs = sorted(cd_runs, key=lambda x: x["created_at"])
        for i, run in enumerate(sorted_runs):
            if run["conclusion"] == "failure":
                for next_run in sorted_runs[i + 1 :]:
                    if next_run["conclusion"] == "success":
                        failed_time = self._parse_datetime(run["created_at"])
                        success_time = self._parse_datetime(next_run["created_at"])
                        mttr_hours = (success_time - failed_time).total_seconds() / 3600
                        break
                if mttr_hours is not None:
                    break

        return {
            "deployments_total": total,
            "deployments_successful": successful,
            "deployments_failed": failed,
            "change_failure_rate_percent": round(change_failure_rate, 2),
            "mttr_hours": round(mttr_hours, 2) if mttr_hours else None,
        }

    def collect_pr_metrics(self) -> dict[str, Any]:
        """Collect PR throughput and lead time metrics."""
        endpoint = f"/repos/{self.repo}/pulls"
        params = {"state": "closed", "sort": "updated", "direction": "desc"}
        prs = self._get_paginated(endpoint, params)

        window_start = self._get_window_start()
        merged_prs = [
            pr
            for pr in prs
            if pr.get("merged_at")
            and self._parse_datetime(pr["merged_at"]) >= window_start
        ]

        lead_times: list[float] = []
        for pr in merged_prs:
            created = self._parse_datetime(pr["created_at"])
            merged = self._parse_datetime(pr["merged_at"])
            lead_times.append((merged - created).total_seconds() / 3600)

        avg_lead_time = sum(lead_times) / len(lead_times) if lead_times else None
        median_lead_time = (
            sorted(lead_times)[len(lead_times) // 2] if lead_times else None
        )

        return {
            "pr_throughput": len(merged_prs),
            "pr_lead_time_avg_hours": round(avg_lead_time, 2)
            if avg_lead_time
            else None,
            "pr_lead_time_median_hours": (
                round(median_lead_time, 2) if median_lead_time else None
            ),
        }

    def collect_ci_metrics(self) -> dict[str, Any]:
        """Collect CI workflow health metrics."""
        ci_runs = self.get_workflow_runs("CI")

        total = len(ci_runs)
        successful = sum(1 for r in ci_runs if r["conclusion"] == "success")
        success_rate = (successful / total * 100) if total > 0 else 0

        durations: list[float] = []
        for run in ci_runs:
            if run.get("run_started_at") and run.get("updated_at"):
                started = self._parse_datetime(run["run_started_at"])
                ended = self._parse_datetime(run["updated_at"])
                durations.append((ended - started).total_seconds() / 60)

        avg_duration = sum(durations) / len(durations) if durations else None

        return {
            "ci_runs_total": total,
            "ci_success_rate_percent": round(success_rate, 2),
            "ci_avg_duration_minutes": round(avg_duration, 2) if avg_duration else None,
        }

    def collect_security_metrics(self) -> dict[str, Any]:
        """Collect security workflow metrics."""
        security_runs = self.get_workflow_runs("Security")

        total = len(security_runs)
        successful = sum(1 for r in security_runs if r["conclusion"] == "success")
        success_rate = (successful / total * 100) if total > 0 else 0

        last_conclusion = None
        if security_runs:
            sorted_runs = sorted(
                security_runs, key=lambda x: x["created_at"], reverse=True
            )
            last_conclusion = sorted_runs[0].get("conclusion")

        return {
            "security_runs_total": total,
            "security_success_rate_percent": round(success_rate, 2),
            "security_last_conclusion": last_conclusion,
        }

    def collect_dependabot_metrics(self) -> dict[str, Any]:
        """Collect Dependabot PR metrics."""
        endpoint = f"/repos/{self.repo}/pulls"
        window_start = self._get_window_start()

        # Open Dependabot PRs
        open_prs = self._get_paginated(endpoint, {"state": "open"})
        dependabot_open = sum(
            1 for pr in open_prs if pr.get("user", {}).get("login") == "dependabot[bot]"
        )

        # Merged Dependabot PRs in window
        closed_prs = self._get_paginated(
            endpoint, {"state": "closed", "sort": "updated", "direction": "desc"}
        )
        dependabot_merged = sum(
            1
            for pr in closed_prs
            if pr.get("user", {}).get("login") == "dependabot[bot]"
            and pr.get("merged_at")
            and self._parse_datetime(pr["merged_at"]) >= window_start
        )

        return {
            "dependabot_prs_open": dependabot_open,
            "dependabot_prs_merged": dependabot_merged,
        }

    def collect_deploy_duration_metrics(self) -> dict[str, Any]:
        """Collect average deploy duration."""
        cd_runs = self.get_workflow_runs("CD - Azure Web App")

        durations: list[float] = []
        for run in cd_runs:
            if (
                run.get("run_started_at")
                and run.get("updated_at")
                and run["conclusion"] == "success"
            ):
                started = self._parse_datetime(run["run_started_at"])
                ended = self._parse_datetime(run["updated_at"])
                durations.append((ended - started).total_seconds() / 60)

        avg_duration = sum(durations) / len(durations) if durations else None

        return {
            "deploy_avg_duration_minutes": (
                round(avg_duration, 2) if avg_duration else None
            ),
        }

    def collect_all_metrics(self) -> dict[str, Any]:
        """Collect all metrics."""
        return {
            "generated_at": datetime.now(UTC).isoformat(),
            "window_days": self.window_days,
            "repository": self.repo,
            "dora": self.collect_dora_metrics(),
            "pull_requests": self.collect_pr_metrics(),
            "ci_health": self.collect_ci_metrics(),
            "deploy_health": self.collect_deploy_duration_metrics(),
            "security": self.collect_security_metrics(),
            "dependabot": self.collect_dependabot_metrics(),
        }


def main() -> None:
    """Main entry point for metrics collection."""
    collector = GitHubMetricsCollector()
    metrics = collector.collect_all_metrics()

    # Ensure site directory exists
    os.makedirs("site", exist_ok=True)

    # Write metrics to JSON
    with open("site/metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print("Metrics collected and written to site/metrics.json")  # noqa: T201
    print(json.dumps(metrics, indent=2))  # noqa: T201


if __name__ == "__main__":
    main()
