# %% [markdown]
# # 1점 투시(one-point perspective)의 핵심을 계산으로 확인하기
#
# 리파의 `Prospettiva`는 눈(펜던트)·작도 도구(컴퍼스·자·직각자·다림추)·거울·명암 옷으로
# "빛과 시각의 학문"을 표현했다. 여기서는 그 중 **화가의 원근법(perspectiva pingendi)**의
# 기하학적 뼈대만 떼어 내 수치로 확인한다.
#
# 구성 요소는 셋뿐이다.
#
# - **시점(eye)** $E$: 원점 $(0,0,0)$에 둔다. 리파의 '사람 눈 펜던트'에 해당한다.
# - **화면(picture plane)**: 시선 방향($z$축)에 수직인 평면 $z = f$. 알베르티의 "창문".
#   $f$는 눈과 화면의 거리(초점거리 / distanza).
# - **소실점(vanishing point)**: 시선에 평행한 모든 직선의 상이 모이는 한 점. 여기서는 $(0,0)$.
#
# 눈에서 점 $P=(x,y,z)$로 향하는 시선(visual ray)이 화면과 만나는 곳이 그 점의 상이다.
# 닮은 삼각형에서 곧바로
#
# $$ \frac{x'}{f} = \frac{x}{z} \quad\Longrightarrow\quad x' = f\,\frac{x}{z},\qquad y' = f\,\frac{y}{z} $$
#
# 이 한 줄이 원근법 전부다. 분모의 $z$ 때문에 **모든 원근 현상이 $1/z$ 법칙으로 환원된다.**

# %%
# 필요 패키지: numpy, plotly, kaleido  (pip install numpy plotly kaleido)
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


F = 1.0  # 눈 ~ 화면 거리 (picture plane at z = F)
EYE_H = 1.6  # 눈높이 (바닥은 y = -EYE_H)


def project(x, y, z, f=F):
    """3D 점 -> 화면 좌표. x' = f x / z, y' = f y / z"""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    z = np.asarray(z, dtype=float)
    return f * x / z, f * y / z


print("f =", F, " eye height =", EYE_H)
print("project(1, 0, 1)  ->", project(1.0, 0.0, 1.0))
print("project(1, 0, 2)  ->", project(1.0, 0.0, 2.0))
print("project(1, 0, 10) ->", project(1.0, 0.0, 10.0))
# 출력: f = 1.0  eye height = 1.6
# 출력: project(1, 0, 1)  -> (np.float64(1.0), np.float64(0.0))
# 출력: project(1, 0, 2)  -> (np.float64(0.5), np.float64(0.0))
# 출력: project(1, 0, 10) -> (np.float64(0.1), np.float64(0.0))
# 해석: 같은 폭이 거리 2배면 화면에서 정확히 1/2로 줄어든다.

# %% [markdown]
# ## 1단계 — 소실점과 지평선은 극한값이다
#
# 바닥면은 $y=-h$ (눈높이 $h$ 아래). 바닥 위에서 시선 방향으로 뻗는 직선
# $(x_0,\,-h,\,z),\ z\to\infty$ 의 상은
#
# $$ x' = f\frac{x_0}{z} \to 0,\qquad y' = f\frac{-h}{z} \to 0 $$
#
# 즉 **$x_0$가 무엇이든 상은 한 점 $(0,0)$으로 수렴한다.** 이것이 소실점이고,
# 바닥 위 모든 수평 방향의 소실점을 모은 높이 $y'=0$이 **지평선**이다.
# 지평선이 언제나 '눈높이'에 오는 이유가 여기서 그대로 나온다.

# %%
z_far = np.array([2.0, 5.0, 10.0, 50.0, 500.0, 1e4])
for x0 in (0.5, 3.0):
    xp, yp = project(x0, -EYE_H, z_far)
    print(f"x0={x0:>4}:  x' =", np.round(xp, 5), " y' =", np.round(yp, 5))
# 출력: x0= 0.5:  x' = [2.5e-01 1.0e-01 5.0e-02 1.0e-02 1.0e-03 5.0e-05]  y' = [-8.0e-01 -3.2e-01 -1.6e-01 -3.2e-02 -3.2e-03 -1.6e-04]
# 출력: x0= 3.0:  x' = [1.5e+00 6.0e-01 3.0e-01 6.0e-02 6.0e-03 3.0e-04]  y' = [-8.0e-01 -3.2e-01 -1.6e-01 -3.2e-02 -3.2e-03 -1.6e-04]
# 해석: 출발 위치 x0가 달라도 z가 커지면 (x', y') -> (0, 0). 소실점은 하나.

# %% [markdown]
# ## 2단계 — 바닥 타일 격자를 화면에 투영
#
# 바닥 $y=-h$ 위에 정사각 타일 격자를 깐다.
#
# - **깊이 방향 선**(시선에 평행, $x=$ 상수): 화면에서 소실점 $(0,0)$으로 수렴한다.
# - **횡방향 선**($z=$ 상수): 화면에서 여전히 **수평 직선**이고, 그 높이는 $y'=-fh/z$.
#   등간격 $z=1,2,3,\dots$ 이 화면에서는 $-fh,\,-fh/2,\,-fh/3,\dots$ 로 **간격이 급격히 좁아진다**.
#
# 화면상의 인접 두 횡선 간격은
#
# $$ \Delta y'(n) = fh\left(\frac{1}{n} - \frac{1}{n+1}\right) = \frac{fh}{n(n+1)} $$
#
# 즉 $n^{-2}$ 로 줄어든다. 이것이 알베르티가 바닥 타일(pavimento)을 그릴 때 얻은
# "같은 크기의 타일이 위로 갈수록 얇아지는" 수열의 정체다.

# %%
n = np.arange(1, 9)
y_rows = -F * EYE_H / n  # z = n 인 횡선의 화면 높이
gaps = np.diff(y_rows)  # 인접 횡선 간격
print("z (m)          :", n)
print("y' (화면 높이) :", np.round(y_rows, 4))
print("간격 Δy'       :", np.round(gaps, 4))
print("이론값 fh/n(n+1):", np.round(F * EYE_H / (n[:-1] * (n[:-1] + 1)), 4))
print("간격 비 Δ(n)/Δ(n+1):", np.round(gaps[:-1] / gaps[1:], 4))
# 출력: z (m)          : [1 2 3 4 5 6 7 8]
# 출력: y' (화면 높이) : [-1.6    -0.8    -0.5333 -0.4    -0.32   -0.2667 -0.2286 -0.2   ]
# 출력: 간격 Δy'       : [0.8    0.2667 0.1333 0.08   0.0533 0.0381 0.0286]
# 출력: 이론값 fh/n(n+1): [0.8    0.2667 0.1333 0.08   0.0533 0.0381 0.0286]
# 출력: 간격 비 Δ(n)/Δ(n+1): [3.     2.     1.6667 1.5    1.4    1.3333]
# 해석: 간격은 fh/(n(n+1)) 공식과 소수점까지 일치. 비율은 (n+2)/n 로 1에 수렴.

# %% [markdown]
# ## 3단계 — 겉보기 크기의 $1/z$ 감소
#
# 실제 높이 $H$인 물체를 거리 $z$에 세우면 화면상 높이는
#
# $$ h'(z) = f\,\frac{H}{z} $$
#
# 이고, 시각(視角)은 $\theta = 2\arctan\!\left(\dfrac{H}{2z}\right)$.
# 가까운 거리에서는 $\theta \approx H/z$ 로 역비례하지만, 아주 가까우면 arctan 때문에 포화한다.
# **거리 2배 → 겉보기 크기 1/2**이 원근법의 체감 법칙이고,
# 리파가 옷의 명암을 "거리에 따른 등급(graduazione)"으로 설명한 것도 같은 계열의 직관이다.

# %%
H = 1.8  # 사람 키
zs = np.array([1.0, 2.0, 4.0, 8.0, 16.0, 32.0])
h_img = F * H / zs
theta = np.degrees(2 * np.arctan(H / (2 * zs)))
for z, hi, th in zip(zs, h_img, theta):
    print(f"z={z:>5.1f} m  ->  화면높이 {hi:.4f}  시각 {th:6.2f}deg")
print("화면높이 비(연속 2배 거리):", np.round(h_img[:-1] / h_img[1:], 4))
# 출력: z=  1.0 m  ->  화면높이 1.8000  시각  83.97deg
# 출력: z=  2.0 m  ->  화면높이 0.9000  시각  48.46deg
# 출력: z=  4.0 m  ->  화면높이 0.4500  시각  25.36deg
# 출력: z=  8.0 m  ->  화면높이 0.2250  시각  12.84deg
# 출력: z= 16.0 m  ->  화면높이 0.1125  시각   6.44deg
# 출력: z= 32.0 m  ->  화면높이 0.0563  시각   3.22deg
# 해석: 화면높이는 정확히 1/2씩(비 = 2.0), 시각은 근거리에서 arctan 때문에 덜 줄어든다.

# %% [markdown]
# ## 4단계 — 시각화 3면
#
# 1. **투영된 바닥 타일 격자** — 깊이선이 소실점으로 모이고 횡선 간격이 $1/n$ 로 압축된다.
# 2. **위에서 본 평면도(top view)** — 눈에서 뻗은 시선과 화면($z=f$)의 교차. 닮은 삼각형이 그대로 보인다.
# 3. **겉보기 크기 곡선** — $h'=fH/z$ 와 시각 $\theta(z)$.

# %%
fig = make_subplots(
    rows=1,
    cols=3,
    subplot_titles=(
        "① 화면 위 바닥 타일 (소실점 수렴)",
        "② 평면도: 시선과 화면 z=f",
        "③ 겉보기 크기 h'=fH/z",
    ),
    specs=[[{}, {}, {"secondary_y": True}]],
    horizontal_spacing=0.08,
)

# --- ① 투영된 격자 -----------------------------------------------------------
x_lines = np.arange(-4, 4.01, 1.0)  # 깊이 방향 선의 x 위치
z_rows = np.arange(1, 21, 1.0)  # 횡선의 z 위치
z_dense = np.geomspace(1.0, 400.0, 300)

for i, x0 in enumerate(x_lines):
    xp, yp = project(x0, -EYE_H, z_dense)
    fig.add_trace(
        go.Scatter(
            x=xp,
            y=yp,
            mode="lines",
            line=dict(color="#3366cc", width=1.4),
            showlegend=(i == 0),
            name="깊이선 (소실점으로)",
            hovertemplate="x'=%{x:.3f}<br>y'=%{y:.3f}<extra></extra>",
        ),
        row=1,
        col=1,
    )

for j, zr in enumerate(z_rows):
    edge = np.array([x_lines[0], x_lines[-1]])
    xp, yp = project(edge, np.full_like(edge, -EYE_H), np.full_like(edge, zr))
    fig.add_trace(
        go.Scatter(
            x=xp,
            y=yp,
            mode="lines",
            line=dict(color="#dc3912", width=1.1),
            showlegend=(j == 0),
            name="횡선 z=const",
            hovertemplate=f"z={zr:.0f}<br>" + "y'=%{y:.4f}<extra></extra>",
        ),
        row=1,
        col=1,
    )

fig.add_trace(
    go.Scatter(
        x=[0],
        y=[0],
        mode="markers+text",
        marker=dict(color="black", size=9, symbol="x"),
        text=["소실점"],
        textposition="top center",
        name="소실점 (0,0)",
    ),
    row=1,
    col=1,
)
fig.add_hline(y=0, line=dict(color="#666", dash="dot"), row=1, col=1)

# --- ② 평면도 ---------------------------------------------------------------
fig.add_trace(
    go.Scatter(
        x=[0],
        y=[0],
        mode="markers+text",
        marker=dict(color="black", size=11),
        text=["눈 E"],
        textposition="middle left",
        name="시점",
        showlegend=False,
    ),
    row=1,
    col=2,
)
fig.add_trace(  # 화면 (z = f)
    go.Scatter(
        x=[F, F],
        y=[-2.6, 2.6],
        mode="lines",
        line=dict(color="#109618", width=3),
        name="화면 z=f",
    ),
    row=1,
    col=2,
)
for x0 in (0.6, 1.6, 2.6):
    for zt in (2.0, 5.0):
        fig.add_trace(  # 시선: 눈 -> 점 (z축을 가로축으로)
            go.Scatter(
                x=[0, zt],
                y=[0, x0],
                mode="lines+markers",
                line=dict(color="#ff9900", width=1.2),
                marker=dict(size=5),
                showlegend=False,
                hovertemplate=f"P=(x={x0}, z={zt})<extra></extra>",
            ),
            row=1,
            col=2,
        )
        xp = F * x0 / zt
        fig.add_trace(
            go.Scatter(
                x=[F],
                y=[xp],
                mode="markers",
                marker=dict(color="#990099", size=8, symbol="diamond"),
                showlegend=False,
                hovertemplate=f"x'={xp:.3f}<extra></extra>",
            ),
            row=1,
            col=2,
        )
fig.add_hline(y=0, line=dict(color="#666", dash="dot"), row=1, col=2)

# --- ③ 겉보기 크기 ----------------------------------------------------------
z_curve = np.linspace(0.5, 30, 400)
fig.add_trace(
    go.Scatter(
        x=z_curve,
        y=F * H / z_curve,
        mode="lines",
        line=dict(color="#3366cc", width=2.5),
        name="화면높이 h'=fH/z",
    ),
    row=1,
    col=3,
)
fig.add_trace(
    go.Scatter(
        x=zs,
        y=h_img,
        mode="markers+text",
        marker=dict(color="#3366cc", size=9),
        text=[f"z={int(z)}" for z in zs],
        textposition="top right",
        showlegend=False,
    ),
    row=1,
    col=3,
)
fig.add_trace(
    go.Scatter(
        x=z_curve,
        y=np.degrees(2 * np.arctan(H / (2 * z_curve))),
        mode="lines",
        line=dict(color="#dc3912", width=2, dash="dash"),
        name="시각 θ(z) [deg]",
    ),
    row=1,
    col=3,
    secondary_y=True,
)

fig.update_xaxes(title_text="x' (화면)", row=1, col=1)
fig.update_yaxes(title_text="y' (화면)", row=1, col=1, range=[-1.85, 0.45])
fig.update_xaxes(title_text="z (깊이)", row=1, col=2, range=[-0.3, 5.6])
fig.update_yaxes(title_text="x (횡방향)", row=1, col=2)
fig.update_xaxes(title_text="z (m)", row=1, col=3, range=[0, 37])
fig.update_yaxes(title_text="화면높이 h'", row=1, col=3, secondary_y=False)
fig.update_yaxes(title_text="시각 θ [deg]", row=1, col=3, secondary_y=True)

fig.update_layout(
    title_text=f"1점 투시의 기하학:  x' = f·x/z  (f={F}, 눈높이 h={EYE_H} m, 사람 키 H={H} m)",
    width=1500,
    height=560,
    template="plotly_white",
    legend=dict(orientation="h", yanchor="bottom", y=-0.24, x=0),
    margin=dict(l=60, r=30, t=90, b=110),
)

_show(fig)

# %%
import os

out_png = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expy.png")
fig.write_image(out_png, scale=2)
print("saved:", out_png, os.path.getsize(out_png), "bytes")
# 출력: saved: <hint dir>/expy.png 318702 bytes

# %% [markdown]
# ## 정리
#
# | 관찰 | 식 | 확인한 수치 |
# |---|---|---|
# | 투영 | $x'=f x/z$ | $x=1$: $z=1\to1.0$, $z=2\to0.5$, $z=10\to0.1$ |
# | 소실점 | $z\to\infty \Rightarrow (x',y')\to(0,0)$ | $x_0=0.5$든 $3.0$이든 $z=10^4$에서 $(5\times10^{-5},\,-1.6\times10^{-4})$ |
# | 지평선 | $y'=0$ (눈높이) | 모든 깊이선의 극한 높이 |
# | 타일 압축 | $\Delta y'(n)=\dfrac{fh}{n(n+1)}$ | $0.8,\,0.2667,\,0.1333,\,0.08,\dots$ (공식과 일치) |
# | 겉보기 크기 | $h'=fH/z$ | 거리 2배마다 정확히 $\times\tfrac12$ |
#
# 리파의 처방과 대응시키면: **눈 펜던트**는 위 계산의 원점 $E$, **자·직각자·다림추**는
# 화면 $z=f$와 지평선 $y'=0$을 세우는 도구, **컴퍼스**는 $1/n$ 수열의 간격을 옮겨 그리는 도구,
# **거울**은 광선의 반사(여기서는 다루지 않은 catoptrica), **명암 옷**은 $1/z$ 감소가
# 선뿐 아니라 밝기·대비에도 적용된다는 사실(공기원근법)에 해당한다.
