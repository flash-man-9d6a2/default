# 필요 패키지: numpy, plotly, kaleido
#   pip install numpy plotly kaleido
#
# 리파 『이코놀로지아』 "PLANEMETRIA" 항목의 도구인
# '야곱의 지팡이(Baccolo di Iacob / cross-staff)'가 어떻게 각을 재고,
# 그 각 두 개("due sole stazioni")로 접근 불가능한 목표까지의 거리를
# 확정하는지를 단계적으로 재현한다.

# %% [markdown]
# # 야곱의 지팡이 — 각도 없이 각을 재는 자
#
# 리파의 원문:
#
# > La Planemetria … dimostra per l'arte militare il pigliare le distanze, larghezze e
# > lontananze, **per dove l'Uomo non si possa accostare** …
# > Le si dà il Baccolo di Iacob, essendo che il detto stromento opera **per via della
# > traversa, che corre innanzi e indietro, con due sole stazioni**.
#
# 도구는 두 부분뿐이다.
#
# * **본체 막대(radius)** — 눈금이 새겨져 있고, 한쪽 끝을 눈에 댄다.
# * **가로대(traversa / transom)** — 본체와 직교하며 **앞뒤로 미끄러진다**. 길이 $L$ 고정.
#
# 가로대의 두 끝이 목표의 두 끝과 정확히 겹쳐 보일 때 멈추고, 눈에서 가로대까지의
# 거리 $d$ 를 **길이 눈금으로 읽는다**. 그러면 시각(視角)은
#
# $$\theta = 2\arctan\!\frac{L/2}{d}$$
#
# 각도기가 전혀 필요 없다는 점이 이 도구의 핵심이다. **길이 한 번 읽기 = 각 한 번 재기.**

# %%
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def _show(fig):
    try:
        from IPython import get_ipython

        if get_ipython() is not None:  # VSCode 셀/Jupyter에서만 렌더링
            fig.show()
    except ImportError:
        pass


INK = "#3f3f46"
MUTED = "#a1a1aa"
C_A = "#3b6fd4"  # 관측점 A
C_B = "#d97706"  # 관측점 B
C_T = "#0f9488"  # 목표(성채)

L = 0.30  # 가로대 길이 [m] — 고정


def angle_from_reading(d, transom=L):
    """가로대 위치 d(눈~가로대 거리, m) -> 시각 theta [rad]"""
    return 2.0 * np.arctan((transom / 2.0) / d)


def reading_from_angle(theta, transom=L):
    """원하는 시각 theta [rad] -> 가로대를 놓아야 할 위치 d [m] (역변환)"""
    return (transom / 2.0) / np.tan(theta / 2.0)


for d in (0.20, 0.30, 0.45, 0.60, 0.90, 1.20):
    th = angle_from_reading(d)
    print(f"d = {d:4.2f} m -> theta = {np.degrees(th):6.2f}deg  (역변환 d = {reading_from_angle(th):4.2f} m)")
# 출력:
# d = 0.20 m -> theta =  73.74deg  (역변환 d = 0.20 m)
# d = 0.30 m -> theta =  53.13deg  (역변환 d = 0.30 m)
# d = 0.45 m -> theta =  36.87deg  (역변환 d = 0.45 m)
# d = 0.60 m -> theta =  28.07deg  (역변환 d = 0.60 m)
# d = 0.90 m -> theta =  18.92deg  (역변환 d = 0.90 m)
# d = 1.20 m -> theta =  14.25deg  (역변환 d = 1.20 m)

# %% [markdown]
# ## 1단계 — 거리를 이미 알 때: 폭(larghezza)을 구한다
#
# 목표까지의 거리 $D$ 를 알고 있다면, 시각 $\theta$ 로부터 목표의 폭은
#
# $$W = 2D\tan\frac{\theta}{2} = D\cdot\frac{L}{d}$$
#
# 삼각함수가 약분되어 **비례식 하나**로 끝난다. 르네상스 측량가가 실제로 쓴 형태다.

# %%
def width_from_angle(D, d, transom=L):
    """거리 D를 알 때 가로대 눈금 d로부터 목표의 폭 W"""
    return D * transom / d


D_known = 250.0  # m
for d in (0.75, 1.00, 1.50):
    print(f"D = {D_known:.0f} m, d = {d:.2f} m -> 목표 폭 W = {width_from_angle(D_known, d):6.2f} m")
# 출력:
# D = 250 m, d = 0.75 m -> 목표 폭 W = 100.00 m
# D = 250 m, d = 1.00 m -> 목표 폭 W =  75.00 m
# D = 250 m, d = 1.50 m -> 목표 폭 W =  50.00 m

# %% [markdown]
# ## 2단계 — 거리를 모를 때: "두 번의 관측(due sole stazioni)"
#
# 각 하나로는 거리가 결정되지 않는다. 접근할 수 없는 성채 $T$ 까지의 거리를 얻으려면
# **길이를 잴 수 있는 기선(base) $\overline{AB}=b$** 를 벌판에 잡고, 양 끝에서 각각
# 야곱의 지팡이로 "상대 관측점 ↔ 성채" 사이의 시각을 잰다.
#
# $$\alpha=\angle TAB,\qquad \beta=\angle TBA,\qquad \gamma=\pi-\alpha-\beta$$
#
# 사인 법칙으로
#
# $$D_A=\overline{AT}=b\,\frac{\sin\beta}{\sin\gamma},\qquad
#   D_B=\overline{BT}=b\,\frac{\sin\alpha}{\sin\gamma}$$
#
# 판화에서 같은 여인이 **전경과 좌측 배경에 두 번** 그려진 이유가 이것이다.

# %%
A = np.array([0.0, 0.0])
B = np.array([200.0, 0.0])  # 기선 b = 200 m (걸음으로 실측 가능한 평지)
T = np.array([140.0, 260.0])  # 접근 불가능한 성채 (검증용 '참값')

b = np.linalg.norm(B - A)


def angle_between(p, q, r):
    """점 p에서 본 q와 r 사이의 각 [rad]"""
    u, v = q - p, r - p
    return np.arccos(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)))


alpha = angle_between(A, B, T)  # A에서 잰 시각
beta = angle_between(B, A, T)  # B에서 잰 시각
gamma = np.pi - alpha - beta

# 지팡이 위에서 실제로 '읽히는' 것은 각이 아니라 가로대 눈금이다
d_A, d_B = reading_from_angle(alpha), reading_from_angle(beta)

print(f"기선 b        = {b:.1f} m")
print(f"A 관측: 가로대 눈금 d = {d_A:.4f} m -> alpha = {np.degrees(alpha):.3f}deg")
print(f"B 관측: 가로대 눈금 d = {d_B:.4f} m -> beta  = {np.degrees(beta):.3f}deg")
print(f"삼각형 닫기:  gamma = {np.degrees(gamma):.3f}deg")
# 출력:
# 기선 b        = 200.0 m
# A 관측: 가로대 눈금 d = 0.2511 m -> alpha = 61.699deg
# B 관측: 가로대 눈금 d = 0.1886 m -> beta  = 77.005deg
# 삼각형 닫기:  gamma = 41.295deg

# %%
D_A = b * np.sin(beta) / np.sin(gamma)
D_B = b * np.sin(alpha) / np.sin(gamma)

print(f"복원한 A->성채 거리 = {D_A:8.3f} m   (참값 {np.linalg.norm(T - A):8.3f} m)")
print(f"복원한 B->성채 거리 = {D_B:8.3f} m   (참값 {np.linalg.norm(T - B):8.3f} m)")
print(f"성채의 지면 높이(수직거리) = {D_A * np.sin(alpha):.3f} m   (참값 {T[1]:.3f} m)")
# 출력:
# 복원한 A->성채 거리 =  295.296 m   (참값  295.296 m)
# 복원한 B->성채 거리 =  266.833 m   (참값  266.833 m)
# 성채의 지면 높이(수직거리) = 260.000 m   (참값 260.000 m)

# %% [markdown]
# ## 3단계 — archipendolo(다림추)가 왜 발치에 놓였는가
#
# 위 식은 전부 **하나의 수평면 위에서** 성립한다. 기선이 기울어 있거나 지팡이가 수평이
# 아니면, 재는 것은 지표면의 길이가 아니라 경사거리가 된다. 경사각 $\phi$ 로 잰
# 기선의 수평 투영은 $b\cos\phi$ 이므로 거리 오차는 곧바로 비례해서 들어온다.

# %%
for phi_deg in (0, 2, 5, 10):
    phi = np.radians(phi_deg)
    D_slope = b * np.cos(phi) * np.sin(beta) / np.sin(gamma)
    print(f"기선 경사 {phi_deg:2d}deg -> 거리 {D_slope:7.2f} m (오차 {D_slope - D_A:+7.2f} m, {100 * (D_slope / D_A - 1):+5.2f}%)")
# 출력:
# 기선 경사  0deg -> 거리  295.30 m (오차   +0.00 m, +0.00%)
# 기선 경사  2deg -> 거리  295.12 m (오차   -0.18 m, -0.06%)
# 기선 경사  5deg -> 거리  294.17 m (오차   -1.12 m, -0.38%)
# 기선 경사 10deg -> 거리  290.81 m (오차   -4.49 m, -1.52%)

# %% [markdown]
# ## 4단계 — 눈금 읽기 오차가 거리에 얼마나 번지는가
#
# 가로대를 1 mm 잘못 놓으면 각이 흔들리고, 그 각이 사인 법칙을 통해 거리로 증폭된다.
# 도구의 실질적 정밀도를 가늠하는 계산이다.

# %%
eps = 0.001  # 가로대 위치 읽기 오차 1 mm


def solve_D(dA, dB, base=b):
    a = angle_from_reading(dA)
    bb = angle_from_reading(dB)
    return base * np.sin(bb) / np.sin(np.pi - a - bb)


base_D = solve_D(d_A, d_B)
for sA, sB in ((+1, 0), (-1, 0), (0, +1), (0, -1), (+1, -1)):
    Dp = solve_D(d_A + sA * eps, d_B + sB * eps)
    print(f"dA {sA:+d}mm, dB {sB:+d}mm -> D = {Dp:7.2f} m ({Dp - base_D:+6.2f} m)")
# 출력:
# dA +1mm, dB +0mm -> D =  294.13 m ( -1.17 m)
# dA -1mm, dB +0mm -> D =  296.49 m ( +1.19 m)
# dA +0mm, dB +1mm -> D =  293.23 m ( -2.07 m)
# dA +0mm, dB -1mm -> D =  297.41 m ( +2.11 m)
# dA +1mm, dB -1mm -> D =  296.22 m ( +0.92 m)

# %% [markdown]
# 1 mm의 손떨림이 약 300 m 거리에서 1~3 m의 오차로 번진다(≈1%).
# 각이 클수록(가로대가 눈에 가까울수록) 같은 1 mm가 더 큰 각 오차가 되므로,
# 실무에서는 **기선을 길게 잡아 두 각을 90°에 가깝지 않게** 만드는 것이 정석이었다.

# %% [markdown]
# ## 그림 — 왼쪽: 시각 측정 원리 / 오른쪽: 두 관측점 삼각측량

# %%
fig = make_subplots(
    rows=1,
    cols=2,
    subplot_titles=(
        "① 가로대 위치 d 를 읽어 시각 θ 를 얻는다",
        "② 두 번의 관측(due stazioni)으로 거리를 닫는다",
    ),
)

# --- 패널 1: 눈 - 본체막대 - 가로대 - 목표
d_demo = 0.55
th_demo = angle_from_reading(d_demo)
reach = 1.20  # 시선 그리는 길이

fig.add_trace(
    go.Scatter(x=[0, 1.25], y=[0, 0], mode="lines", line=dict(color=INK, width=3), name="본체 막대", showlegend=False),
    row=1, col=1,
)
for tick in np.arange(0.1, 1.26, 0.1):  # 눈금
    fig.add_trace(
        go.Scatter(x=[tick, tick], y=[-0.02, 0.02], mode="lines", line=dict(color=MUTED, width=1), showlegend=False),
        row=1, col=1,
    )
fig.add_trace(
    go.Scatter(
        x=[d_demo, d_demo], y=[-L / 2, L / 2], mode="lines+markers",
        line=dict(color=C_B, width=4), marker=dict(size=9, color=C_B),
        name="가로대 (traversa)",
    ),
    row=1, col=1,
)
for sgn in (+1, -1):
    fig.add_trace(
        go.Scatter(
            x=[0, reach], y=[0, sgn * (L / 2) * reach / d_demo],
            mode="lines", line=dict(color=C_A, width=2, dash="dot"),
            name="시선", showlegend=(sgn > 0),
        ),
        row=1, col=1,
    )
fig.add_trace(
    go.Scatter(
        x=[reach, reach], y=[-(L / 2) * reach / d_demo, (L / 2) * reach / d_demo],
        mode="lines", line=dict(color=C_T, width=6), name="목표의 폭 W",
    ),
    row=1, col=1,
)
fig.add_trace(
    go.Scatter(x=[0], y=[0], mode="markers+text", marker=dict(size=12, color=INK),
               text=["눈"], textposition="middle left", showlegend=False),
    row=1, col=1,
)
fig.add_annotation(
    x=d_demo / 2, y=0.055, xref="x", yref="y", text=f"d = {d_demo:.2f} m",
    showarrow=False, font=dict(size=12, color=INK),
    bgcolor="rgba(255,255,255,0.92)", row=1, col=1,
)
fig.add_annotation(
    x=d_demo, y=L / 2 + 0.06, xref="x", yref="y", text=f"L = {L:.2f} m (고정)",
    showarrow=False, font=dict(size=12, color=C_B), row=1, col=1,
)
fig.add_annotation(
    x=0.19, y=-0.045, xref="x", yref="y",
    text=f"θ = {np.degrees(th_demo):.1f}°", showarrow=False,
    font=dict(size=14, color=C_A), bgcolor="rgba(255,255,255,0.92)", row=1, col=1,
)
fig.add_annotation(
    x=reach, y=(L / 2) * reach / d_demo + 0.05, xref="x", yref="y",
    text="목표", showarrow=False, font=dict(size=12, color=C_T), row=1, col=1,
)

# --- 패널 2: 삼각측량
fig.add_trace(
    go.Scatter(x=[A[0], B[0]], y=[A[1], B[1]], mode="lines",
               line=dict(color=INK, width=3), name=f"기선 b = {b:.0f} m"),
    row=1, col=2,
)
fig.add_trace(
    go.Scatter(x=[A[0], T[0]], y=[A[1], T[1]], mode="lines",
               line=dict(color=C_A, width=2, dash="dot"), name=f"A→T  {D_A:.1f} m"),
    row=1, col=2,
)
fig.add_trace(
    go.Scatter(x=[B[0], T[0]], y=[B[1], T[1]], mode="lines",
               line=dict(color=C_B, width=2, dash="dot"), name=f"B→T  {D_B:.1f} m"),
    row=1, col=2,
)
fig.add_trace(
    go.Scatter(x=[A[0], B[0]], y=[A[1], B[1]], mode="markers+text",
               marker=dict(size=13, color=[C_A, C_B]), text=["A", "B"],
               textposition="bottom center", showlegend=False),
    row=1, col=2,
)
fig.add_trace(
    go.Scatter(x=[T[0]], y=[T[1]], mode="markers+text", marker=dict(size=15, color=C_T, symbol="square"),
               text=["성채 T (접근 불가)"], textposition="top center", showlegend=False),
    row=1, col=2,
)
fig.add_annotation(x=A[0] + 34, y=A[1] + 14, text=f"α = {np.degrees(alpha):.1f}°",
                   showarrow=False, font=dict(size=13, color=C_A), row=1, col=2)
fig.add_annotation(x=B[0] - 40, y=B[1] + 16, text=f"β = {np.degrees(beta):.1f}°",
                   showarrow=False, font=dict(size=13, color=C_B), row=1, col=2)
fig.add_annotation(x=T[0] - 30, y=T[1] - 32, text=f"γ = {np.degrees(gamma):.1f}°",
                   showarrow=False, font=dict(size=13, color=C_T), bgcolor="rgba(255,255,255,0.92)", row=1, col=2)

fig.update_xaxes(title_text="본체 막대 눈금 [m]", row=1, col=1, zeroline=False, range=[-0.15, 1.42],
                 gridcolor="rgba(0,0,0,0.06)", showline=True, linecolor=MUTED)
fig.update_yaxes(row=1, col=1, scaleanchor="x", scaleratio=1, zeroline=False,
                 gridcolor="rgba(0,0,0,0.06)", showline=False, title_text="가로대 방향 [m]")
fig.update_xaxes(title_text="동서 [m]", row=1, col=2, zeroline=False,
                 gridcolor="rgba(0,0,0,0.06)", showline=True, linecolor=MUTED)
fig.update_yaxes(title_text="남북 [m]", row=1, col=2, scaleanchor="x2", scaleratio=1,
                 zeroline=False, gridcolor="rgba(0,0,0,0.06)")
fig.update_layout(
    title="야곱의 지팡이(Baccolo di Iacob) — 리파 『이코놀로지아』 Planemetria",
    template="plotly_white",
    width=1180,
    height=560,
    font=dict(color=INK, size=13),
    legend=dict(orientation="h", yanchor="bottom", y=-0.22, x=0),
    margin=dict(l=60, r=30, t=80, b=110),
)

_show(fig)

import os

_here = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
_png = os.path.join(_here, "expy.png")
fig.write_image(_png, scale=2)
print("saved", os.path.basename(_png))
# 출력: saved expy.png
