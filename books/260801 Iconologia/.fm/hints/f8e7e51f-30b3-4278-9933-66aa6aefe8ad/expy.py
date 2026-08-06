# %% [markdown]
# # Orografia — 그노몬의 그림자로 시각을 읽는 원리
#
# 리파의 `OROGRAFIA`(시각 측정술)는 **왼손에 해시계**를 들고, 머리 위 태양의 광선이
# **그노몬(Gnomone)의 그림자**를 만들어 *"l'ombra del Gnomone, diretta all' ora corrente"*
# — 곧 현재 시각을 가리키게 한다.
#
# 이 노트북은 그 장치를 실제 천문 계산으로 재현한다.
#
# 1. 태양의 고도·방위각을 **위도 $\phi$ · 적위 $\delta$ · 시간각 $H$** 로부터 구한다
# 2. 극축에 맞춘 스타일(style)의 그림자가 만드는 **수평 해시계 시각선 공식**
#    $$\tan\theta = \sin\phi \,\tan H$$
#    을 유도하고 수치로 검증한다
# 3. 수직 막대(원시적 그노몬)의 그림자 끝 궤적을 계절별로 그린다
#
# 리파가 여인의 오른손에 쥐어 준 **컴퍼스·자·경사계(declinatorio)**는 바로 이 시각선을
# 문자판 위에 작도하기 위한 도구다.

# %%
# 필요 패키지: numpy, plotly, kaleido
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


PHI_DEG = 41.9  # 로마(리파가 활동한 도시)의 위도
PHI = np.radians(PHI_DEG)
print(f"위도 phi = {PHI_DEG} deg (Roma)")
# 출력: 위도 phi = 41.9 deg (Roma)

# %% [markdown]
# ## 1. 시간각과 적위
#
# * **시간각** $H$ : 진태양시 $t$(시)에 대해 $H = 15^\circ \times (t - 12)$.
#   정오에 $0$, 오후는 양(서쪽), 오전은 음(동쪽).
# * **적위** $\delta$ : 하지 $+23.44^\circ$, 분점 $0^\circ$, 동지 $-23.44^\circ$.
#
# 지평좌표(ENU: East–North–Up)에서 태양의 단위벡터는
#
# $$
# \begin{aligned}
# s_{U} &= \sin\phi\sin\delta + \cos\phi\cos\delta\cos H \quad (=\sin a,\; a=\text{고도})\\
# s_{E} &= -\cos\delta\sin H\\
# s_{N} &= \sin\delta\cos\phi - \cos\delta\cos H\sin\phi
# \end{aligned}
# $$


# %%
def hour_angle(t_hours):
    """진태양시(시) -> 시간각(rad). 정오 = 0, 오후 = +"""
    return np.radians(15.0 * (np.asarray(t_hours, dtype=float) - 12.0))


def sun_vector(H, delta, phi=PHI):
    """ENU 좌표계의 태양 단위벡터 (E, N, U)"""
    sE = -np.cos(delta) * np.sin(H)
    sN = np.sin(delta) * np.cos(phi) - np.cos(delta) * np.cos(H) * np.sin(phi)
    sU = np.sin(phi) * np.sin(delta) + np.cos(phi) * np.cos(delta) * np.cos(H)
    return np.array([sE, sN, sU])


def altitude_azimuth(H, delta, phi=PHI):
    """고도(deg), 방위각(deg, 북=0 동=90 남=180 서=270)"""
    sE, sN, sU = sun_vector(H, delta, phi)
    alt = np.degrees(np.arcsin(sU))
    az = np.degrees(np.arctan2(sE, sN)) % 360.0
    return alt, az


# 위생 검사: 분점 정오의 태양은 정남(방위 180도), 고도 = 90 - phi
alt, az = altitude_azimuth(hour_angle(12.0), 0.0)
print(f"분점 정오  고도={alt:.2f} 방위={az:.2f}  (기대 고도 {90 - PHI_DEG:.2f}, 방위 180)")
# 출력: 분점 정오  고도=48.10 방위=180.00  (기대 고도 48.10, 방위 180)

for t in [6.0, 9.0, 15.0, 18.0]:
    a, z = altitude_azimuth(hour_angle(t), 0.0)
    print(f"  분점 {t:>4.1f}시 -> 고도 {a:6.2f} deg, 방위 {z:7.2f} deg")
# 출력:   분점  6.0시 -> 고도   0.00 deg, 방위  90.00 deg
# 출력:   분점  9.0시 -> 고도  31.76 deg, 방위 123.74 deg
# 출력:   분점 15.0시 -> 고도  31.76 deg, 방위 236.26 deg
# 출력:   분점 18.0시 -> 고도   0.00 deg, 방위 270.00 deg
# (분점에는 정확히 정동에서 뜨고 정서로 진다 -> 방위 90 / 270)

# %% [markdown]
# ## 2. 수평 해시계 시각선 공식의 유도
#
# 해시계의 **스타일(style)**은 지축(천구 북극)과 평행해야 한다. ENU에서 그 방향은
# $p = (0,\ \cos\phi,\ \sin\phi)$ — 즉 북쪽으로 위도만큼 기울어진 막대다.
#
# 스타일 위의 점 $P = t\,p$ 의 그림자는 $P - \dfrac{P_U}{s_U}\,s$ 로 지평면에 떨어진다. 계산하면
#
# $$
# X_E = t\,\frac{\sin\phi\cos\delta\sin H}{s_U},\qquad
# Y_N = t\,\frac{\cos\delta\cos H}{s_U}
# $$
#
# 따라서 정오선(북쪽 $+Y$)에서 잰 그림자 각도 $\theta$ 는
#
# $$
# \tan\theta = \frac{X_E}{Y_N} = \frac{\sin\phi\sin H}{\cos H} = \boxed{\sin\phi\,\tan H}
# $$
#
# **$\delta$ 가 소거된다** — 계절에 관계없이 같은 시각선을 쓸 수 있다는 것이 극축 스타일의 요체다.
# (그림자가 오후에 $+E$ 쪽으로 가는 것은 맞다: 오후 태양은 서쪽에 있으므로 그림자는 동쪽으로 눕는다.)


# %%
def hour_line_angle_analytic(H, phi=PHI):
    """수평 해시계 시각선 각도(deg). 정오선에서 잰 각, 오후 = +"""
    return np.degrees(np.arctan2(np.sin(phi) * np.sin(H), np.cos(H)))


def hour_line_angle_numeric(H, delta, phi=PHI):
    """극축 스타일의 그림자를 실제로 투영해 얻은 각도(deg)"""
    p = np.array([0.0, np.cos(phi), np.sin(phi)])  # 스타일 방향(천구 북극)
    s = sun_vector(H, delta, phi)
    if s[2] <= 0:
        return np.nan  # 해가 지평선 아래
    shadow = p - (p[2] / s[2]) * s  # (E, N, 0)
    return np.degrees(np.arctan2(shadow[0], shadow[1]))


print(f"{'시각':>5} {'H(deg)':>8} {'해석식':>9} {'하지 δ=+23.44':>14} {'분점 δ=0':>11} {'동지 δ=-23.44':>14}")
for t in [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]:
    H = hour_angle(t)
    row = [hour_line_angle_numeric(H, np.radians(d)) for d in (23.44, 0.0, -23.44)]
    print(f"{t:>5} {np.degrees(H):>8.1f} {hour_line_angle_analytic(H):>9.3f} " + " ".join(f"{v:>14.3f}" for v in row))
# 출력:    시각   H(deg)       해석식    하지 δ=+23.44      분점 δ=0    동지 δ=-23.44
# 출력:     7    -75.0   -68.138        -68.138        -68.138            nan
# 출력:     8    -60.0   -49.156        -49.156        -49.156        -49.156
# 출력:     9    -45.0   -33.736        -33.736        -33.736        -33.736
# 출력:    10    -30.0   -21.085        -21.085        -21.085        -21.085
# 출력:    11    -15.0   -10.145        -10.145        -10.145        -10.145
# 출력:    12      0.0     0.000          0.000          0.000          0.000
# 출력:    13     15.0    10.145         10.145         10.145         10.145
# 출력:    14     30.0    21.085         21.085         21.085         21.085
# 출력:    15     45.0    33.736         33.736         33.736         33.736
# 출력:    16     60.0    49.156         49.156         49.156         49.156
# 출력:    17     75.0    68.138         68.138         68.138            nan
# -> 해가 떠 있는 모든 경우에 해석식과 완전히 일치. 적위 delta 는 실제로 소거된다.
#    (동지 7시/17시의 nan 은 로마 위도에서 그 시각에 해가 아직/이미 지평선 아래라는 뜻)

# %%
# 계절 무관성의 정량 검증
errs = []
for t in np.arange(6.5, 17.6, 0.25):
    H = hour_angle(t)
    for d in np.linspace(-23.44, 23.44, 9):
        v = hour_line_angle_numeric(H, np.radians(d))
        if not np.isnan(v):
            errs.append(abs(v - hour_line_angle_analytic(H)))
print(f"표본 {len(errs)}개, 최대 오차 = {max(errs):.3e} deg")
# 출력: 표본 387개, 최대 오차 = 1.421e-14 deg  (부동소수점 한계 = 정확히 성립)

# 위도에 따른 시각선 압축: 적도(phi=0)면 모든 시각선이 겹치고, 극(phi=90)이면 등간격 15도
for phi_deg in [0, 20, 41.9, 60, 90]:
    angles = [hour_line_angle_analytic(hour_angle(t), np.radians(phi_deg)) for t in (13, 14, 15)]
    print(f"  phi={phi_deg:>5.1f} deg -> 13,14,15시 시각선 = " + ", ".join(f"{a:6.2f}" for a in angles))
# 출력:   phi=  0.0 deg -> 13,14,15시 시각선 =   0.00,   0.00,   0.00
# 출력:   phi= 20.0 deg -> 13,14,15시 시각선 =   5.24,  11.17,  18.88
# 출력:   phi= 41.9 deg -> 13,14,15시 시각선 =  10.15,  21.09,  33.74
# 출력:   phi= 60.0 deg -> 13,14,15시 시각선 =  13.06,  26.57,  40.89
# 출력:   phi= 90.0 deg -> 13,14,15시 시각선 =  15.00,  30.00,  45.00
# -> sin(phi) 가 15도 간격을 압축하는 계수. 적도에서는 수평 해시계가 무용지물이 된다.

# %% [markdown]
# ## 3. 수직 막대 그노몬의 그림자 끝 궤적
#
# 높이 $h$ 의 **수직** 막대(가장 원시적인 그노몬)의 그림자 끝은
#
# $$
# (X_E,\ Y_N) = -\frac{h}{s_U}\,(s_E,\ s_N)
# $$
#
# 이 궤적은 하루 동안 **원뿔곡선**을 그린다: 분점에는 직선(동서선), 하지에는 북쪽으로 볼록한 쌍곡선,
# 동지에는 남쪽으로 볼록한 쌍곡선. 그리고 그림자의 **방향(각도)이 계절마다 달라지므로**
# 수직 막대만으로는 시각을 정확히 읽을 수 없다 — 리파의 그노몬이 극축으로 기울어져야 하는 이유다.


# %%
def vertical_gnomon_shadow(t_hours, delta_deg, h=1.0, phi=PHI):
    """수직 막대 그림자 끝 좌표 (E, N). 해가 지평선 아래면 nan"""
    H = hour_angle(t_hours)
    sE, sN, sU = sun_vector(H, np.radians(delta_deg), phi)
    ok = sU > np.radians(3.0)  # 고도 3도 미만은 그림자가 발산 -> 잘라냄
    X = np.where(ok, -h * sE / np.where(ok, sU, 1.0), np.nan)
    Y = np.where(ok, -h * sN / np.where(ok, sU, 1.0), np.nan)
    return X, Y


for d, name in [(23.44, "하지"), (0.0, "분점"), (-23.44, "동지")]:
    X, Y = vertical_gnomon_shadow(np.array([12.0]), d)
    ang = np.degrees(np.arctan2(X[0], Y[0]))
    print(f"{name}(δ={d:+6.2f}) 정오 그림자 길이 = {np.hypot(X[0], Y[0]):.4f} h, 방향 = {ang:.1f} deg (북)")
# 출력: 하지(δ=+23.44) 정오 그림자 길이 = 0.3338 h, 방향 = 0.0 deg (북)
# 출력: 분점(δ= +0.00) 정오 그림자 길이 = 0.8972 h, 방향 = 0.0 deg (북)
# 출력: 동지(δ=-23.44) 정오 그림자 길이 = 2.1782 h, 방향 = 0.0 deg (북)
# -> 동지 정오의 그림자는 하지의 6.5배. 정오 방향은 계절과 무관하게 항상 정북.

# 같은 '오후 3시'라도 수직 막대의 그림자 각도는 계절마다 크게 다르다
print("\n오후 3시 그림자 방향 (정오선에서 잰 각, deg)")
for d, name in [(23.44, "하지"), (0.0, "분점"), (-23.44, "동지")]:
    X, Y = vertical_gnomon_shadow(np.array([15.0]), d)
    print(f"  {name}: {np.degrees(np.arctan2(X[0], Y[0])):7.2f}   (극축 스타일이면 항상 {hour_line_angle_analytic(hour_angle(15.0)):.2f})")
# 출력: 오후 3시 그림자 방향 (정오선에서 잰 각, deg)
# 출력:   하지:   78.06   (극축 스타일이면 항상 33.74)
# 출력:   분점:   56.26   (극축 스타일이면 항상 33.74)
# 출력:   동지:   41.65   (극축 스타일이면 항상 33.74)
# -> 같은 오후 3시인데 방향이 36도 넘게 벌어진다. 수직 막대는 계절 보정 없이 시계가 될 수 없다.

# %% [markdown]
# ## 4. 그림
#
# * **왼쪽** — 로마 위도의 수평 해시계 문자판. 6시~18시 시각선을 $\tan\theta=\sin\phi\tan H$ 로 작도.
#   리파의 여인이 든 **컴퍼스와 자**가 하는 일이 바로 이 작도다.
# * **오른쪽** — 높이 1인 수직 막대의 그림자 끝 궤적(하지/분점/동지)과 정오 위치.

# %%
fig = make_subplots(
    rows=1,
    cols=2,
    subplot_titles=(
        f"수평 해시계 시각선 (phi = {PHI_DEG} deg)",
        "수직 그노몬 그림자 끝 궤적",
    ),
    horizontal_spacing=0.12,
)

# --- 왼쪽: 시각선 ---
R = 1.0
for t in range(6, 19):
    th = np.radians(hour_line_angle_analytic(hour_angle(t)))
    # 6시/18시는 동서선 위에 정확히 눕는다
    x, y = R * np.sin(th), R * np.cos(th)
    fig.add_trace(
        go.Scatter(
            x=[0, x], y=[0, y], mode="lines",
            line=dict(color="#8c6d3f" if t != 12 else "#b03a2e", width=3 if t == 12 else 1.6),
            hovertemplate=f"{t}시 · theta={np.degrees(th):.2f} deg<extra></extra>",
            showlegend=False,
        ),
        row=1, col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=[1.12 * x], y=[1.12 * y], mode="text", text=[str(t)],
            textfont=dict(size=12, color="#5b4a2f"), showlegend=False, hoverinfo="skip",
        ),
        row=1, col=1,
    )

# 스타일(극축 막대)의 지평면 투영 = 정오선
fig.add_trace(
    go.Scatter(x=[0, 0], y=[0, 0.55], mode="lines",
               line=dict(color="#1f4e79", width=6), name="스타일(극축) 투영"),
    row=1, col=1,
)
# 문자판 테두리(위쪽 반원 — 시각선이 놓이는 범위)
ang = np.linspace(-np.pi / 2, np.pi / 2, 400)
fig.add_trace(
    go.Scatter(x=R * np.sin(ang), y=R * np.cos(ang), mode="lines",
               line=dict(color="#c9b79c", width=1), showlegend=False, hoverinfo="skip"),
    row=1, col=1,
)

# --- 오른쪽: 그림자 끝 궤적 ---
ts = np.linspace(4.0, 20.0, 800)
for d, name, color in [(23.44, "하지 δ=+23.44", "#d1495b"),
                       (0.0, "분점 δ=0", "#3f7d20"),
                       (-23.44, "동지 δ=-23.44", "#2a6f97")]:
    X, Y = vertical_gnomon_shadow(ts, d)
    fig.add_trace(
        go.Scatter(x=X, y=Y, mode="lines", name=name, line=dict(color=color, width=2.5),
                   hovertemplate="E=%{x:.2f}h, N=%{y:.2f}h<extra>" + name + "</extra>"),
        row=1, col=2,
    )
    Xn, Yn = vertical_gnomon_shadow(np.array([15.0]), d)
    fig.add_trace(
        go.Scatter(x=Xn, y=Yn, mode="markers", marker=dict(color=color, size=10, symbol="circle"),
                   name=f"{name.split()[0]} 15시", showlegend=False,
                   hovertemplate="15시<extra>" + name + "</extra>"),
        row=1, col=2,
    )
fig.add_trace(
    go.Scatter(x=[0], y=[0], mode="markers+text", marker=dict(color="#333", size=11, symbol="x"),
               text=["그노몬"], textposition="bottom center", showlegend=False),
    row=1, col=2,
)

fig.update_xaxes(title_text="동쪽 →   [ tan(theta) = sin(phi)·tan(H) ]", row=1, col=1,
                 range=[-1.35, 1.35], zeroline=False)
fig.update_yaxes(title_text="북쪽 ↑", row=1, col=1, range=[-0.30, 1.32],
                 scaleanchor="x", scaleratio=1, zeroline=False)
fig.update_xaxes(title_text="동쪽 → (그노몬 높이 배수)   [ 계절마다 방향이 달라진다 ]", row=1, col=2,
                 range=[-4.5, 4.5])
fig.update_yaxes(title_text="북쪽 ↑", row=1, col=2, range=[-2.3, 4.5],
                 scaleanchor="x2", scaleratio=1)
fig.update_layout(
    title=dict(text="Orografia — 그노몬의 그림자가 시각을 가리키는 원리", x=0.5, xanchor="center", y=0.97),
    template="plotly_white", width=1180, height=620,
    margin=dict(t=140, b=90),
    legend=dict(orientation="h", y=-0.16, x=0.5, xanchor="center"),
)
# subplot 제목이 메인 타이틀과 겹치지 않도록 아래로 내린다
for ann in fig.layout.annotations[:2]:
    ann.update(y=0.90, yanchor="bottom")

_show(fig)
fig.write_image("expy.png", scale=2)
print("saved expy.png")
# 출력: saved expy.png

# %% [markdown]
# ## 정리
#
# | 리파의 도상 | 대응하는 수학 |
# |---|---|
# | 머리 위 **태양** | 적위 $\delta$ 와 시간각 $H$ 로 정해지는 태양 방향 벡터 |
# | **그노몬의 그림자** | 지평면 투영 $P - (P_U/s_U)\,s$ |
# | 왼손의 **해시계** 문자판 | $\tan\theta = \sin\phi\tan H$ 로 그린 시각선 다발 |
# | 오른손의 **컴퍼스·자** | 그 시각선·자오선·분점선·회귀선의 작도 |
# | 오른손의 **경사계(declinatorio)** | 벽면의 방위·편각 $\to$ 수직 해시계의 시각선 보정 |
# | 머리 위 **모래시계** | 해가 없는 밤 ($s_U < 0$) 의 시간 측정 |
#
# 핵심: $\delta$ 가 시각선 공식에서 소거되기 때문에 **하나의 문자판이 사시사철 통한다**.
# 그 대가로 그노몬은 반드시 **위도 $\phi$ 만큼 기울어 천구 북극을 향해야** 한다.
