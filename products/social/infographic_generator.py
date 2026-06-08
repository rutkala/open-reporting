#!/usr/bin/env python3
import json
import argparse
import sys
import plotly.graph_objects as go


def parse_args():
    parser = argparse.ArgumentParser(description="Generate Social Infographic from Anomaly JSON")
    parser.add_argument("--payload", type=str, required=True, help="JSON payload string")
    parser.add_argument("--output", type=str, default="infographic.png", help="Output path")
    return parser.parse_args()


def generate_infographic(payload: dict, output_path: str):
    metric = payload.get("metric", "Unknown Metric")
    value = payload.get("value", 0.0)
    mean = payload.get("historical_mean", 0.0)
    z_score = payload.get("z_score", 0.0)

    # Dark mode premium palette
    bg_color = "#0B0E14"
    card_bg = "rgba(21, 26, 34, 0.6)"
    card_border = "rgba(255, 255, 255, 0.1)"
    text_color = "#F1F5F9"
    accent_color = "#3B82F6" if z_score < 0 else "#EF4444"
    muted_color = "#64748B"

    fig = go.Figure()

    # Glassmorphism background card
    fig.add_shape(
        type="rect",
        xref="paper", yref="paper",
        x0=0.05, y0=0.05, x1=0.95, y1=0.95,
        fillcolor=card_bg,
        line=dict(color=card_border, width=2),
        layer="below"
    )

    # Historical Mean Bar
    fig.add_trace(
        go.Bar(
            name="Historical Mean",
            x=["Historical Mean", "Current Value"],
            y=[mean, 0],
            marker_color=muted_color,
            width=0.4,
            text=[f"{mean:.1f}", ""],
            textposition="outside",
            textfont=dict(size=36, color=text_color, family="Inter")
        )
    )

    # Current Value Bar
    fig.add_trace(
        go.Bar(
            name="Current Value",
            x=["Historical Mean", "Current Value"],
            y=[0, value],
            marker_color=accent_color,
            width=0.4,
            text=["", f"{value:.1f}"],
            textposition="outside",
            textfont=dict(size=48, color=accent_color, family="Inter")
        )
    )

    # Annotations and layout adjustments
    fig.update_layout(
        title=dict(
            text=f"<b>{metric.upper()}</b> ANOMALY",
            font=dict(size=64, color=text_color, family="Inter"),
            x=0.5,
            y=0.88,
            xanchor="center",
            yanchor="top"
        ),
        annotations=[
            dict(
                text=f"Z-Score: {z_score:.2f}",
                x=0.5,
                y=0.80,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=42, color=accent_color, family="Inter"),
                bgcolor="rgba(0,0,0,0.5)",
                borderpad=15,
                bordercolor=card_border,
                borderwidth=1,
            )
        ],
        width=1080,
        height=1350,
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        showlegend=False,
        margin=dict(l=120, r=120, t=350, b=150),
        barmode="group",
    )

    fig.update_xaxes(
        showgrid=False,
        tickfont=dict(size=36, color=text_color, family="Inter"),
        linecolor=muted_color,
        linewidth=2,
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor=card_border,
        zerolinecolor=muted_color,
        zerolinewidth=2,
        tickfont=dict(size=28, color=muted_color, family="Inter"),
    )

    fig.write_image(output_path, scale=1)
    print(f"Successfully generated infographic: {output_path}")


def main():
    args = parse_args()
    try:
        payload = json.loads(args.payload)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON payload: {e}")
        sys.exit(1)

    generate_infographic(payload, args.output)


if __name__ == "__main__":
    main()
