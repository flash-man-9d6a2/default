# 필요 패키지: numpy, plotly, kaleido
#   pip install numpy plotly kaleido
# 실행: python3 expy.py  (또는 VSCode / Jupyter에서 셀 단위 실행)

# %% [markdown]
# # 「사랑의 기원」 도상의 화경(火鏡) 광학 — 단계별 실험
#
# 카스텔리니가 『이코놀로지아』 「Origine di Amore」에서 세운 비유:
#
# > *siccome per lo specchio, **occhio dell'arte**, posto incontro all'occhio del Sole,
# > passando i raggi solari si accende la facella, così per gli occhi nostri,
# > **specchi della natura**, ... la facella di amore **nel cuor** si accende.*
#
# 이 비유의 "발판"은 은유가 아니라 검증 가능한 물리다. 아래에서 그 물리를 직접 계산한다.
#
# 1. 얇은 렌즈 공식으로 태양광의 상이 어디에 생기는지 확인
# 2. 평행광선 다발의 광선추적(ray tracing)
# 3. 태양의 유한 각지름 때문에 초점이 "점"이 아니라 스폿인 것
# 4. 집광비 $(D/d)^2$ 와 발화 임계
# 5. 아르키메데스 거울이 왜 어려운지 같은 식으로 확인
# 6. 광학 → 연애 심리 대응표

# %%
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def _show(fig):
    try:
        from IPython import get_ipython

        if get_ipython() is not None:
            fig.show()
    except ImportError:
        pass


# --- 물리 상수 / 태양 파라미터 ---------------------------------------------
THETA_SUN = 9.30e-3  # 태양 각지름 [rad] (= 0.533도). 초점 스폿 크기를 결정한다.
G_SUN = 1000.0  # 지표면 태양조도 [W/m^2] (AM1.5 근사)
SIGMA = 5.670374419e-8  # 스테판-볼츠만 상수 [W/m^2/K^4]
Q_IGNITE = 25e3  # 목재 자연발화 열유속 [W/m^2] (~25 kW/m^2)
Q_TINDER = 10e3  # 부싯깃/숯천 착화 열유속 [W/m^2] (~10 kW/m^2)

print(f"태양 각지름 theta = {THETA_SUN * 1e3:.2f} mrad = {np.degrees(THETA_SUN):.3f} deg")
print(f"이론 최대 집광비 C_max = 1/sin^2(theta/2) = {1 / np.sin(THETA_SUN / 2) ** 2:,.0f}")
# 출력:
# 태양 각지름 theta = 9.30 mrad = 0.533 deg
# 이론 최대 집광비 C_max = 1/sin^2(theta/2) = 46,248

# %% [markdown]
# ## 1. 얇은 렌즈 공식 — 태양의 상은 초점면에 생긴다
#
# $$\frac{1}{f} = \frac{1}{s_o} + \frac{1}{s_i}
#   \quad\Longrightarrow\quad
#   s_i = \frac{f\,s_o}{s_o - f}$$
#
# 태양은 $s_o \to \infty$ 이므로 $s_i \to f$. 즉 **상은 정확히 초점면**에 놓인다.
# 도판의 여인이 렌즈를 앞뒤로 조정해 "가장 작은 점"을 찾는 행위가 바로 이 면을 찾는 것이다.

# %%
def image_distance(f, s_o):
    """얇은 렌즈 공식으로 상거리 s_i 를 구한다. s_o = inf 이면 s_i = f."""
    if np.isinf(s_o):
        return f
    return f * s_o / (s_o - f)


F_LENS = 0.20  # 손에 드는 화경의 초점거리 [m]
D_LENS = 0.10  # 렌즈 지름 [m]

for s_o in [1.0, 10.0, 1e3, 1.496e11, np.inf]:  # 마지막 유한값은 1 AU
    s_i = image_distance(F_LENS, s_o)
    label = "무한(∞)" if np.isinf(s_o) else f"{s_o:.3e} m"
    print(f"s_o = {label:>14s}  ->  s_i = {s_i:.9f} m   (f = {F_LENS} m)")
# 출력:
# s_o =        1.000e+00 m  ->  s_i = 0.250000000 m   (f = 0.2 m)
# s_o =        1.000e+01 m  ->  s_i = 0.204081633 m   (f = 0.2 m)
# s_o =        1.000e+03 m  ->  s_i = 0.200040008 m   (f = 0.2 m)
# s_o =        1.496e+11 m  ->  s_i = 0.200000000 m   (f = 0.2 m)
# s_o =           무한(∞)  ->  s_i = 0.200000000 m   (f = 0.2 m)
#  -> 1 AU 거리에서 이미 s_i 와 f 는 소수점 9자리까지 구별되지 않는다.

# %% [markdown]
# ## 2. 광선추적 — 평행광선이 초점에 모인다
#
# 얇은 렌즈 근사에서 렌즈면($x=0$)에 높이 $y$로 들어온 평행광선은
# 굴절 후 항상 초점 $(f, 0)$을 향한다. 즉 광선의 기울기는 $-y/f$.
#
# 태양의 원반 양 끝에서 오는 광선은 $\pm\theta_\odot/2$ 만큼 기울어져 들어오므로
# 초점면 위 $y = \mp f\,\theta_\odot/2$ 에 모인다 → 이것이 스폿의 지름을 만든다.

# %%
def trace_parallel_bundle(f, D, tilt=0.0, n_rays=9):
    """평행광선 다발의 광선추적.

    Returns: list of (xs, ys) — 렌즈 앞(입사) + 렌즈 뒤(굴절) 경로.
    tilt: 입사광선의 기울기 [rad]. 태양 원반 끝은 ±theta/2.
    """
    ys_in = np.linspace(-D / 2, D / 2, n_rays)
    x_before, x_after = -1.6 * f, 1.9 * f
    paths = []
    for y0 in ys_in:
        # 렌즈면(x=0)에 도달하는 높이: 기울어진 입사광선
        y_lens = y0
        y_start = y_lens - tilt * x_before  # x_before는 음수
        # 굴절 후: 기울어진 평행광은 초점면의 (f, -tilt*f) 로 모인다
        y_focus = -tilt * f
        slope_out = (y_focus - y_lens) / f
        paths.append(
            (
                np.array([x_before, 0.0, x_after]),
                np.array([y_start, y_lens, y_lens + slope_out * x_after]),
            )
        )
    return paths, (-tilt * f)


paths_axis, yf_axis = trace_parallel_bundle(F_LENS, D_LENS, tilt=0.0)
paths_top, yf_top = trace_parallel_bundle(F_LENS, D_LENS, tilt=+THETA_SUN / 2, n_rays=3)
paths_bot, yf_bot = trace_parallel_bundle(F_LENS, D_LENS, tilt=-THETA_SUN / 2, n_rays=3)

d_spot = F_LENS * THETA_SUN
print(f"축상 광선 수렴점 y = {yf_axis:.6f} m")
print(f"태양 원반 끝 광선 수렴점 y = {yf_top * 1e3:+.3f} mm, {yf_bot * 1e3:+.3f} mm")
print(f"=> 스폿 지름 d = f*theta = {d_spot * 1e3:.3f} mm  (검증: {abs(yf_top - yf_bot) * 1e3:.3f} mm)")
# 출력:
# 축상 광선 수렴점 y = -0.000000 m
# 태양 원반 끝 광선 수렴점 y = -0.930 mm, +0.930 mm
# => 스폿 지름 d = f*theta = 1.860 mm  (검증: 1.860 mm)

# %% [markdown]
# ## 3. 스폿 크기와 집광비
#
# $$d = f\,\theta_\odot, \qquad
#   C = \left(\frac{D}{d}\right)^2 = \left(\frac{D}{f\theta_\odot}\right)^2
#     = \frac{1}{(N\theta_\odot)^2}, \qquad N \equiv \frac{f}{D}$$
#
# **핵심: 집광비는 렌즈의 절대 크기가 아니라 f수 $N$ 으로만 결정된다.**
# 큰 렌즈가 센 것이 아니라 "밝은"(f수 작은) 렌즈가 세다.

# %%
def spot_diameter(f):
    """초점 스폿 지름 [m] (기하광학 한계, 회절/수차 무시)."""
    return f * THETA_SUN


def concentration(D, f):
    """집광비 C = (D/d)^2."""
    return (D / spot_diameter(f)) ** 2


def concentration_from_fnumber(N):
    return 1.0 / (N * THETA_SUN) ** 2


print(f"{'f [cm]':>8s} {'d [mm]':>8s} {'N=f/D':>7s} {'C':>10s} {'조도 [MW/m^2]':>14s}")
rows = []
for f_cm in [5, 10, 20, 40, 80]:
    f = f_cm / 100
    C = concentration(D_LENS, f)
    rows.append((f_cm, spot_diameter(f) * 1e3, f / D_LENS, C, C * G_SUN / 1e6))
    print(f"{rows[-1][0]:8.0f} {rows[-1][1]:8.3f} {rows[-1][2]:7.1f} {rows[-1][3]:10,.0f} {rows[-1][4]:14.2f}")
# 출력 (D = 10 cm 고정):
#   f [cm]   d [mm]   N=f/D          C  조도 [MW/m^2]
#        5    0.465     0.5     46,248          46.25
#       10    0.930     1.0     11,562          11.56
#       20    1.860     2.0      2,891           2.89
#       40    3.720     4.0        723           0.72
#       80    7.440     8.0        181           0.18

# %%
# 크기가 달라도 f수가 같으면 집광비가 같다는 것을 확인
for D, f in [(0.05, 0.10), (0.10, 0.20), (0.40, 0.80), (2.00, 4.00)]:
    print(f"D={D:5.2f} m, f={f:5.2f} m -> N={f / D:.1f}, C={concentration(D, f):,.0f}")
# 출력:
# D= 0.05 m, f= 0.10 m -> N=2.0, C=2,891
# D= 0.10 m, f= 0.20 m -> N=2.0, C=2,891
# D= 0.40 m, f= 0.80 m -> N=2.0, C=2,891
# D= 2.00 m, f= 4.00 m -> N=2.0, C=2,891
#  -> 렌즈를 키워도 f수가 같으면 스폿의 '세기'는 그대로다. 커지는 것은 스폿의 넓이(=총 출력)뿐.

# %% [markdown]
# ## 4. 발화 임계와 복사평형 온도
#
# 발화에 필요한 것은 온도가 아니라 **열유속(irradiance)** 이다.
# 부싯깃/숯천은 $\sim10\ \mathrm{kW/m^2}$, 목재 자연발화는 $\sim25\ \mathrm{kW/m^2}$ 정도가 필요하므로
# 필요한 집광비는
#
# $$C_{\text{필요}} = \frac{q''_{\text{ign}}}{G_\odot}$$
#
# 즉 **고작 10~25배**다. 손에 드는 화경($C \approx 2900$)은 100배 이상 여유가 있다.
#
# 도달 가능한 복사평형 온도는 (손실 무시, $\varepsilon = 1$)
#
# $$T = \left(\frac{C\,G_\odot}{\varepsilon\sigma}\right)^{1/4}$$

# %%
def eq_temperature(C, emissivity=1.0):
    return (C * G_SUN / (emissivity * SIGMA)) ** 0.25


C_need_tinder = Q_TINDER / G_SUN
C_need_wood = Q_IGNITE / G_SUN
print(f"부싯깃 착화 필요 집광비  C >= {C_need_tinder:.0f}")
print(f"목재 자연발화 필요 집광비 C >= {C_need_wood:.0f}")

C_hand = concentration(D_LENS, F_LENS)
print(f"\n손 화경 (D=10cm, f=20cm): C = {C_hand:,.0f}  ({C_hand / C_need_wood:.0f}배 여유)")
print(f"  조도 = {C_hand * G_SUN / 1e6:.2f} MW/m^2,  복사평형 T = {eq_temperature(C_hand):,.0f} K "
      f"({eq_temperature(C_hand) - 273:,.0f} °C)")
for C in [10, 100, 1000, 2890, 46246]:
    print(f"  C = {C:>6,d} -> T = {eq_temperature(C):7,.0f} K")
# 출력:
# 부싯깃 착화 필요 집광비  C >= 10
# 목재 자연발화 필요 집광비 C >= 25
#
# 손 화경 (D=10cm, f=20cm): C = 2,891  (116배 여유)
#   조도 = 2.89 MW/m^2,  복사평형 T = 2,672 K (2,399 °C)
#   C =     10 -> T =     648 K
#   C =    100 -> T =   1,152 K
#   C =  1,000 -> T =   2,049 K
#   C =  2,890 -> T =   2,672 K
#   C = 46,246 -> T =   5,344 K
#   (주: T는 emissivity=1, 대류/전도 손실 0 가정의 상한값)

# %% [markdown]
# ## 5. 아르키메데스 거울은 왜 어려운가 — 같은 식으로 확인
#
# 카스텔리니는 "아르키메데스가 이것으로 시라쿠사를 포위한 로마 함선을 태웠다"고 쓴다.
# 그러나 $d = f\theta_\odot$ 이 문제다. 표적이 멀면 $f$ 가 커지고 스폿도 **비례해서** 커진다.
#
# 필요한 반사면 총 면적:
#
# $$A_{\text{mirror}} = \frac{q''_{\text{ign}} \cdot A_{\text{spot}}}{\rho\,G_\odot},
#   \qquad A_{\text{spot}} = \frac{\pi}{4}(R\,\theta_\odot)^2$$
#
# ($\rho$ = 청동 거울 반사율, 낙관적으로 0.6)

# %%
def archimedes_requirement(R, q_need=Q_IGNITE, reflectivity=0.6):
    """거리 R [m]의 표적을 발화시키는 데 필요한 거울 총면적."""
    d = R * THETA_SUN
    A_spot = np.pi / 4 * d**2
    A_mirror = q_need * A_spot / (reflectivity * G_SUN)
    return d, A_spot, A_mirror


print(f"{'거리 R [m]':>10s} {'스폿 d [m]':>11s} {'스폿면적 [m^2]':>14s} {'필요 거울면적 [m^2]':>19s} {'0.5m 거울 개수':>14s}")
for R in [10, 30, 50, 100, 150]:
    d, A_s, A_m = archimedes_requirement(R)
    n = A_m / (0.5 * 0.5)
    print(f"{R:10.0f} {d:11.3f} {A_s:14.4f} {A_m:19.2f} {n:14.0f}")
# 출력:
#  거리 R [m]  스폿 d [m]  스폿면적 [m^2]  필요 거울면적 [m^2]   0.5m 거울 개수
#         10       0.093         0.0068                0.28                1
#         30       0.279         0.0611                2.55               10
#         50       0.465         0.1698                7.08               28
#        100       0.930         0.6793               28.30              113
#        150       1.395         1.5284               63.68              255
#
# 면적만 보면 '가능해 보인다'는 것이 이 전승이 끈질기게 살아남은 이유다. 실제 장벽은 따로 있다:
#  (1) 수십~수백 장을 오차 없이 '같은 한 점'에 겹쳐 조준해야 한다
#  (2) 태양은 15 deg/h 로 움직이고 배는 파도로 흔들린다 -> 수십초~수분간 조준 유지가 불가능
#  (3) 젖은 나무는 발화 열유속이 훨씬 높다
#  (4) 50~100 m는 이미 화살/투석 사거리 안 -> 전술적으로 무의미
# MIT(2005) / MythBusters 재현: 정지·건조 표적 + 완벽한 조준에서만 발화, 전투 조건에서는 실패.

# %%
# 카스텔리니가 인용한 전거들의 실제 장치 종류 — 렌즈(굴절) vs 오목거울(반사)
sources = [
    ("도판의 물건 (specchio trasparente, grosso)", "볼록렌즈 (굴절)", "광선이 '통과' — 비유에 필수"),
    ("오론스 피네 De speculo ustorio (1551)", "포물면 오목거울 (반사)", "제목이 speculum ustorium"),
    ("플루타르코스 누마 9 — 베스타 성화", "금속 오목거울 (반사)", "직각이등변삼각형 회전면"),
    ("조나라스 — 프로클로스, 콘스탄티노플 515", "오목거울 (반사)", "실제 주인공은 아르키메데스가 아님"),
    ("아르키메데스, 시라쿠사 기원전 212", "오목거울 (전승)", "동시대 사료 전무, 최초 언급 6세기"),
]
print(f"{'전거':<42s} {'장치':<20s} 비고")
print("-" * 100)
for a, b, c in sources:
    print(f"{a:<42s} {b:<20s} {c}")
# 출력: 도판만 굴절(렌즈)이고 인용된 전거는 전부 반사(오목거울)다.
#       -> 카스텔리니는 성질이 다른 두 장치를 specchio 한 단어로 묶었다.
#          비유가 '광선이 눈을 통과해 심장에 닿는' 그림을 요구했기 때문이다.

# %% [markdown]
# ## 6. 대응표: 광학(자연학) → 연애 심리(도덕학)
#
# 비유는 4항 비례식이다.
#
# $$\frac{\text{렌즈 (occhio dell'arte)}}{\text{태양}}
#   \;=\;
#   \frac{\text{우리 눈 (specchi della natura)}}{\text{연인의 눈}}
#   \;\Longrightarrow\;
#   \frac{\text{초점의 횃불}}{\;} = \frac{\text{심장의 사랑}}{\;}$$

# %%
mapping = [
    ("광원 (태양)", "우상단 인격 태양", "연인의 눈 = un bel Sole", "미(美)가 원인"),
    ("평행 태양광선", "빗살 광선", "spezie / spiriti (피치노)", "사랑은 실체 전달"),
    ("굴절체 (렌즈)", "오른손의 투명 원반", "우리 눈", "눈은 집광 장치"),
    ("정렬 incontro", "태양을 향해 든 팔", "시선의 마주침 rincontro", "안 마주치면 안 붙는다"),
    ("초점 (f)", "광선 수렴점", "심장", "사랑의 자리"),
    ("착화된 표적", "왼손의 facella", "incendium", "한순간 → 지속 연소"),
    ("f수 N = f/D", "(도판에 없음)", "응시의 집중·근접", "강도는 거리에 달렸다"),
]
w = (18, 20, 26)
print(f"{'광학':<{w[0]}s} {'도상 요소':<{w[1]}s} {'연애 심리':<{w[2]}s} 도덕적 함의")
print("-" * 100)
for a, b, c, d in mapping:
    print(f"{a:<{w[0]}s} {b:<{w[1]}s} {c:<{w[2]}s} {d}")

print("\n모토: SIC IN CORDE FACIT AMOR INCENDIUM  (Plautus, Mercator)")
print("판화 리본에는 FACIT 이 생략되어 SIC IN CORDE / AMOR INCENDIVM 으로 새겨져 있다.")
# 출력: (위 4열 표가 그대로 출력된다)

# %% [markdown]
# ### 남는 균열
# 도판의 렌즈는 빛이 **들어오는** 수용(intromission) 모델인데,
# 본문의 피치노–플라톤 생리학은 눈이 광선을 **쏘아 보내는** 방출(extramission) 모델이다
# (*"saetti … le frezze de' raggi suoi"*, *"congiungono i lumi con lumi"*).
# 도상은 단방향 집광을, 텍스트는 쌍방향 광선 교환을 그린다.

# %% [markdown]
# ## 7. 종합 시각화

# %%
fig = make_subplots(
    rows=2,
    cols=2,
    subplot_titles=(
        "① 광선추적: 평행 태양광 → 초점의 횃불",
        "② 초점거리 vs 스폿 지름 d = f·θ",
        "③ f수 vs 집광비 C = 1/(Nθ)²",
        "④ 집광비 vs 복사평형 온도",
    ),
    horizontal_spacing=0.11,
    vertical_spacing=0.14,
)

# ---- ① 광선추적 -----------------------------------------------------------
for i, (xs, ys) in enumerate(paths_axis):
    fig.add_trace(
        go.Scatter(x=xs, y=ys * 1e3, mode="lines", line=dict(color="#e8a33d", width=1.6),
                   name="태양광선 (원반 중심)", legendgroup="ax", showlegend=(i == 0)),
        row=1, col=1,
    )
for grp, paths, col in [("top", paths_top, "#c0504d"), ("bot", paths_bot, "#4472c4")]:
    for i, (xs, ys) in enumerate(paths):
        fig.add_trace(
            go.Scatter(x=xs, y=ys * 1e3, mode="lines",
                       line=dict(color=col, width=1.0, dash="dot"),
                       name=f"태양 원반 {'상' if grp == 'top' else '하'}단 (±θ/2)",
                       legendgroup=grp, showlegend=(i == 0)),
            row=1, col=1,
        )
# 렌즈 실루엣 (두 개의 원호)
t = np.linspace(-1, 1, 60)
bulge = 0.055 * F_LENS
lens_x = np.concatenate([bulge * (1 - t**2), -bulge * (1 - t[::-1] ** 2)])
lens_y = np.concatenate([t, t[::-1]]) * (D_LENS / 2) * 1e3
fig.add_trace(
    go.Scatter(x=lens_x, y=lens_y, mode="lines", fill="toself",
               line=dict(color="#3b7dd8", width=2), fillcolor="rgba(120,180,255,0.35)",
               name="렌즈 (occhio dell'arte)"),
    row=1, col=1,
)
# 초점 스폿 = 횃불
fig.add_trace(
    go.Scatter(x=[F_LENS], y=[0], mode="markers+text",
               marker=dict(symbol="star", size=16, color="#d1402a"),
               text=[f"  facella (d={d_spot * 1e3:.2f} mm)"], textposition="top right",
               textfont=dict(size=10), name="초점 = 심장 = 횃불"),
    row=1, col=1,
)
fig.add_hline(y=0, line=dict(color="rgba(128,128,128,0.5)", width=1, dash="dash"), row=1, col=1)
fig.update_xaxes(title_text="광축 x [m]  (f = 0.20 m)", row=1, col=1)
fig.update_yaxes(title_text="높이 y [mm]", row=1, col=1)

# ---- ② 스폿 지름 ----------------------------------------------------------
f_grid = np.linspace(0.02, 1.0, 200)
fig.add_trace(
    go.Scatter(x=f_grid * 100, y=spot_diameter(f_grid) * 1e3, mode="lines",
               line=dict(color="#3b7dd8", width=2.5), name="d = f·θ", showlegend=False),
    row=1, col=2,
)
fig.add_trace(
    go.Scatter(x=[F_LENS * 100], y=[d_spot * 1e3], mode="markers+text",
               marker=dict(size=11, color="#d1402a"),
               text=[f" 손 화경 {d_spot * 1e3:.2f} mm"], textposition="top left",
               textfont=dict(size=10), showlegend=False),
    row=1, col=2,
)
fig.update_xaxes(title_text="초점거리 f [cm]", row=1, col=2)
fig.update_yaxes(title_text="스폿 지름 d [mm]", row=1, col=2)

# ---- ③ f수 vs 집광비 -----------------------------------------------------
N_grid = np.linspace(0.5, 30, 400)
fig.add_trace(
    go.Scatter(x=N_grid, y=concentration_from_fnumber(N_grid), mode="lines",
               line=dict(color="#3b7dd8", width=2.5), name="C = 1/(Nθ)²", showlegend=False),
    row=2, col=1,
)
# 주의: plotly 의 add_hline 은 log 축 subplot 에서 좌표를 잘못 잡는다(10^y 로 해석).
#       그래서 임계선은 Scatter 트레이스로 직접 그린다.
for y, lab, col, side in [
    (C_need_tinder, f"부싯깃 착화 C≈{C_need_tinder:.0f}", "#7f9c3f", "left"),
    (C_need_wood, f"목재 발화 C≈{C_need_wood:.0f}", "#c0504d", "right"),
    (1 / np.sin(THETA_SUN / 2) ** 2, "이론 상한 C≈46,000", "#888888", "right"),
]:
    fig.add_trace(
        go.Scatter(x=[N_grid[0], N_grid[-1]], y=[y, y], mode="lines",
                   line=dict(color=col, width=1.3, dash="dot"), showlegend=False,
                   hovertemplate=f"{lab}<extra></extra>"),
        row=2, col=1,
    )
    fig.add_trace(
        go.Scatter(x=[N_grid[0] if side == "left" else N_grid[-1]], y=[y],
                   mode="text", text=[" " + lab + " "],
                   textposition="top right" if side == "left" else "top left",
                   textfont=dict(size=10, color=col),
                   showlegend=False, hoverinfo="skip"),
        row=2, col=1,
    )
fig.add_trace(
    go.Scatter(x=[F_LENS / D_LENS], y=[C_hand], mode="markers+text",
               marker=dict(size=11, color="#d1402a"),
               text=[f" 손 화경 N=2, C={C_hand:,.0f}"], textposition="middle right",
               textfont=dict(size=10), showlegend=False),
    row=2, col=1,
)
fig.update_xaxes(title_text="f수  N = f/D", row=2, col=1)
fig.update_yaxes(title_text="집광비 C", type="log", range=[0, np.log10(2e5)], row=2, col=1)

# ---- ④ 집광비 vs 온도 ----------------------------------------------------
C_grid = np.logspace(0, np.log10(46246), 300)
fig.add_trace(
    go.Scatter(x=C_grid, y=eq_temperature(C_grid), mode="lines",
               line=dict(color="#3b7dd8", width=2.5),
               name="T = (CG/σ)^¼", showlegend=False),
    row=2, col=2,
)
for C, lab in [(C_need_wood, "목재 발화 임계"), (C_hand, "손 화경")]:
    fig.add_trace(
        go.Scatter(x=[C], y=[eq_temperature(C)], mode="markers+text",
                   marker=dict(size=11, color="#d1402a"),
                   text=[f" {lab} {eq_temperature(C):,.0f} K"], textposition="top left",
                   textfont=dict(size=10), showlegend=False),
        row=2, col=2,
    )
fig.add_hline(y=1173, line=dict(color="#7f9c3f", width=1.2, dash="dot"),
              annotation_text="목재 발화점 ~900 °C 영역", annotation_position="bottom right",
              annotation_font=dict(size=9, color="#7f9c3f"), row=2, col=2)
fig.update_xaxes(title_text="집광비 C", type="log", row=2, col=2)
fig.update_yaxes(title_text="복사평형 온도 T [K]", row=2, col=2)

fig.update_layout(
    title=dict(
        text="화경(burning glass) 광학 — 「Origine di Amore」의 물리적 발판<br>"
             "<sub>SIC IN CORDE FACIT AMOR INCENDIUM · 태양 각지름 θ = 9.30 mrad, G = 1000 W/m²</sub>",
        x=0.5, xanchor="center",
    ),
    height=900, width=1400, template="plotly_white",
    legend=dict(orientation="h", yanchor="bottom", y=-0.09, xanchor="center", x=0.5),
    margin=dict(t=110, b=90),
)

_show(fig)

# %%
import os

_out = os.path.join(os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else ".", "expy.png")
fig.write_image(_out, scale=2)
print("saved:", _out)
# 출력: saved: .../5d956047-b172-4f11-82ac-e2b10475b248/expy.png

# %% [markdown]
# ## 정리
#
# - 얇은 렌즈 공식에서 태양($s_o\to\infty$)의 상은 **초점면**에 생긴다 — 도판의 여인이 찾는 면.
# - 태양의 각지름 때문에 초점은 점이 아니라 $d = f\theta_\odot$ 의 **스폿**이다.
# - 집광비 $C = 1/(N\theta_\odot)^2$ 는 **f수만의 함수** — 손 화경으로도 $C\approx2900$,
#   목재 발화 임계($C\approx25$)의 100배 이상. **비유의 발판은 실제 물리로 튼튼하다.**
# - 반면 아르키메데스 거울은 $d = R\theta_\odot$ 때문에 원리적으로 불가능한 건 아니지만
#   조준 유지·표적 습도·전술적 무의미로 실전에서는 성립하지 않고, 사료도 후대 전승뿐이다.
# - 인용된 전거(피네·플루타르코스·조나라스)는 모두 **오목거울(반사)** 이야기인데
#   도판의 물건은 **렌즈(굴절)** 다. 비유가 "광선이 눈을 통과해 심장에 닿는" 그림을
#   요구했기 때문에 광학적 정확성이 밀린 것이다.
