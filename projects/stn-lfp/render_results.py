"""Rebuild the public STN-LFP figure from aggregate CSV tables only."""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")


ROOT = Path(__file__).resolve().parent
BLUE, ORANGE = "#0072B2", "#D55E00"


def read_rows(name):
    with (ROOT / name).open() as stream:
        return list(csv.DictReader(stream))


def plot_panel(axis, rows, labels, title, highlight=None):
    for index, (row, label) in enumerate(zip(rows, labels)):
        mean, low, high = (
            float(row[key]) for key in ("mean_subject_ba", "ci_low", "ci_high")
        )
        if not 0 <= low <= mean <= high <= 1:
            raise ValueError(f"Invalid result interval: {row}")
        axis.errorbar(
            mean,
            index,
            xerr=[[mean - low], [high - mean]],
            fmt="o",
            color=ORANGE if index == highlight else BLUE,
            markersize=6,
            linewidth=1.5,
            capsize=3,
        )
        axis.text(1.015, index, f"{mean:.3f}", va="center", fontsize=10)
    axis.set_yticks(range(len(labels)), labels)
    axis.set_ylim(len(labels) - 0.5, -0.5)
    axis.set_xlim(0.4, 1)
    axis.axvline(0.5, color="0.5", linestyle="--", linewidth=1)
    axis.grid(axis="x", alpha=0.25)
    axis.spines[["top", "right"]].set_visible(False)
    axis.set_title(title, loc="left", fontsize=12, fontweight="bold", pad=12)


def main():
    import matplotlib.pyplot as plt

    representation = {
        row["variant"]: row
        for row in read_rows("representation_results.csv")
        if row["perturbation_seed"] == "-1"
    }
    temporal = {
        row["panel"]: row
        for row in read_rows("temporal_results.csv")
        if row["budget"] == "full" and row["block_windows"] == "0"
    }
    blocks = {row["block_windows"]: row for row in read_rows("block_results.csv")}
    with plt.rc_context(
        {
            "font.size": 10,
            "svg.fonttype": "none",
            "svg.hashsalt": "stn-lfp-public-results",
        }
    ):
        figure, axes = plt.subplots(2, 1, figsize=(10, 7.4))
        figure.subplots_adjust(left=0.33, right=0.91, top=0.88, bottom=0.1, hspace=0.65)
        figure.suptitle(
            "STN-LFP medication-state decoding",
            fontsize=16,
            fontweight="bold",
            y=0.99,
        )
        figure.text(
            0.5,
            0.94,
            "Mean patient-level balanced accuracy · 95% bootstrap intervals · 28 participants",
            ha="center",
            fontsize=10,
        )
        variants = (
            "spectral_mean",
            "spectral_distribution",
            "spectral_temporal",
            "bandpower_temporal",
            "nested_selection",
        )
        plot_panel(
            axes[0],
            [representation[key] for key in variants],
            [
                "Spectral means",
                "Distribution only",
                "Full temporal, fixed candidate",
                "Relative powers and ratios",
                "Nested selection, 12 candidates",
            ],
            "A  Representation and model selection",
            highlight=4,
        )
        plot_panel(
            axes[1],
            [
                temporal["complete"],
                temporal["global_change"],
                temporal["local_continuity"],
                blocks["1"],
                blocks["30"],
            ],
            [
                "Full temporal, original order",
                "Distribution + global change",
                "Distribution + local continuity",
                "Shuffle: one-window blocks",
                "Shuffle: 30-window blocks",
            ],
            "B  Temporal components and perturbations",
        )
        axes[1].set_xlabel("Mean balanced accuracy")
        figure.text(
            0.5,
            0.025,
            "Dashed line: chance (0.5). Fixed and nested procedures are distinct. "
            "Shuffle summaries average five seeds within each participant.",
            ha="center",
            fontsize=8,
        )
        for extension in ("png", "svg"):
            destination = ROOT / f"results.{extension}"
            figure.savefig(
                destination,
                dpi=300,
                bbox_inches="tight",
                facecolor="white",
                metadata={"Date": None} if extension == "svg" else {},
            )
            if extension == "svg":
                destination.write_text(
                    "\n".join(
                        line.rstrip() for line in destination.read_text().splitlines()
                    )
                    + "\n"
                )
        plt.close(figure)


if __name__ == "__main__":
    main()
