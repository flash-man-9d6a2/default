# %% [markdown]
# # 카스텔리니의 '밤' 논증을 천문 기하로 검증하기
#
# 카스텔리니(Giovanni Zaratino Castellini)는 리파 『이코놀로지아』의 **Notte(밤)** 항목 부록에서
# "밤은 대지의 그림자(*ombra della terra*)"라는 통설을 세 갈래로 반박한다.
#
# | # | 카스텔리니의 주장 | 아리스토텔레스적 술어 | 이 노트에서 검증할 것 |
# |---|---|---|---|
# | 1 | 밤의 작용인은 *그림자*가 아니라 **불투명하고 조밀한 대지의 몸** | causa efficiens | 원뿔의 밑면 반지름이 $R_E$로 고정 → 차폐체가 원뿔을 만든다 |
# | 2 | 오히려 **진 태양**이 밤(그리고 그림자)의 원인 | causa efficiens | 원뿔의 길이 $L$이 $R_S, d$에만 의존 → 태양이 도형을 결정 |
# | 3 | 밤은 그림자의 *결과*가 아니라 **원인**. 그림자는 "특정한 도형"을 본질에 포함하지만 밤은 그렇지 않다 | privatio / forma | $R_S$를 바꾸면 도형은 원뿔↔원기둥↔확산뿔로 바뀌지만 '빛 없음'은 그대로 |
#
# 3번을 카스텔리니는 이렇게 적었다:
#
# > *l'ombra … contenendo essenzialmente … certa e determinata figura … ma la Notte non include
# > necessariamente in se tal figura … dato che la terra non cagionasse alcun' ombra e figura,
# > nientedimeno per la semplice tenebra e privazione del lume, sarebbe Notte.*
#
# 즉 **밤 = privatio lucis(빛의 결여)**, 그림자 = 그 결여가 "특정 크기와 도형으로 한정된(contratta e ristretta)" 경우.
# 아래에서 표준 천문 상수로 이 구분이 실제 기하와 어떻게 맞물리는지 계산한다.

# %%
# 필요 패키지: plotly, kaleido  (pip install plotly kaleido)
# numpy 없이 표준 math 만으로 계산한다.
import math

def _show(fig):
    try:
        from IPython import get_ipython
        if get_ipython() is not None:  # VSCode 셀/Jupyter에서만 렌더링
            fig.show()
    except ImportError:
        pass


# --- 표준 천문 상수 (IAU 2015 nominal values) ---
R_SUN = 695_700.0        # 태양 반지름 [km]
R_EARTH = 6_371.0        # 지구 평균 반지름 [km]
AU = 149_597_870.7       # 천문단위 = 태양-지구 평균거리 [km]
D_MOON = 384_400.0       # 지구-달 평균거리 [km]

print(f"R_Sun   = {R_SUN:,.0f} km")
print(f"R_Earth = {R_EARTH:,.0f} km   (R_Sun / R_Earth = {R_SUN/R_EARTH:.1f})")
print(f"1 AU    = {AU:,.1f} km")
# 출력: R_Sun   = 695,700 km
# 출력: R_Earth = 6,371 km   (R_Sun / R_Earth = 109.2)
# 출력: 1 AU    = 149,597,870.7 km

# %% [markdown]
# ## 1. 본영(umbra) 원뿔의 꼭짓점 거리
#
# 태양(반지름 $R_S$)과 지구(반지름 $R_E$)의 **외접 공통접선**은 지구 뒤쪽 축상 한 점에서 만난다.
# 태양 중심을 원점, 지구 중심을 $x=d$에 두면 닮은 삼각형에서
#
# $$\frac{R_S}{d + L} = \frac{R_E}{L} \quad\Longrightarrow\quad L = \frac{R_E \, d}{R_S - R_E}$$
#
# 이 $L$이 **본영 원뿔의 길이**(지구 중심에서 원뿔 꼭짓점까지)다. 축을 따라 거리 $x$에서의 본영 반지름은
#
# $$r_u(x) = R_E\left(1 - \frac{x}{L}\right)$$
#
# 반영(penumbra)은 **내접 공통접선**이 만드는 확산 원뿔이다:
#
# $$r_p(x) = R_E + x \cdot \frac{R_S + R_E}{d}$$
#
# 여기서 눈여겨볼 점 — $x=0$에서 두 반지름 모두 $R_E$다. **도형의 밑면은 차폐체(대지)가 정한다**(반박 1).
# 반면 원뿔이 얼마나 빨리 닫히는지($1/L$)와 얼마나 벌어지는지($(R_S+R_E)/d$)는
# **오직 태양의 $R_S$와 거리 $d$가 정한다**(반박 2).

# %%
def umbra_length(R_s=R_SUN, R_e=R_EARTH, d=AU):
    """본영 원뿔 길이 L = R_e * d / (R_s - R_e).
    R_s > R_e -> 양수(수렴 원뿔), R_s == R_e -> inf(원기둥), R_s < R_e -> 음수(발산 원뿔)."""
    if R_s == R_e:
        return math.inf
    return R_e * d / (R_s - R_e)


def umbra_radius(x, R_s=R_SUN, R_e=R_EARTH, d=AU):
    L = umbra_length(R_s, R_e, d)
    return R_e if math.isinf(L) else R_e * (1.0 - x / L)  # L=inf → 원기둥


def penumbra_radius(x, R_s=R_SUN, R_e=R_EARTH, d=AU):
    return R_e + x * (R_s + R_e) / d


L = umbra_length()
print(f"본영 원뿔 길이 L        = {L:,.0f} km  = {L/1e6:.3f} x 10^6 km")
print(f"  (알려진 값 약 1.38 x 10^6 km  -> 일치: {abs(L/1e6 - 1.38) < 0.01})")
print(f"  달 거리의 배수        = {L/D_MOON:.2f} x  (달은 원뿔 안쪽 약 {D_MOON/L*100:.1f}% 지점)")
print(f"본영 원뿔 반각          = {math.degrees(math.atan(R_EARTH/L))*60:.2f} arcmin")
# 출력: 본영 원뿔 길이 L        = 1,382,632 km  = 1.383 x 10^6 km
# 출력:   (알려진 값 약 1.38 x 10^6 km  -> 일치: True)
# 출력:   달 거리의 배수        = 3.60 x  (달은 원뿔 안쪽 약 27.8% 지점)
# 출력: 본영 원뿔 반각          = 15.84 arcmin

# %%
# 달 거리에서의 단면 -- 월식 관측으로 검증 가능한 값
ru_moon = umbra_radius(D_MOON)
rp_moon = penumbra_radius(D_MOON)
print(f"달 거리({D_MOON:,.0f} km)에서")
print(f"  본영 반지름 r_u = {ru_moon:,.0f} km   (알려진 값 약 4,600 km)")
print(f"  반영 반지름 r_p = {rp_moon:,.0f} km   (알려진 값 약 8,200 km)")
print(f"  본영 지름 / 달 지름 = {2*ru_moon/(2*1737.4):.2f}  -> 개월식 때 달이 본영에 완전히 잠김")
# 출력: 달 거리(384,400 km)에서
# 출력:   본영 반지름 r_u = 4,600 km   (알려진 값 약 4,600 km)
# 출력:   반영 반지름 r_p = 8,175 km   (알려진 값 약 8,200 km)
# 출력:   본영 지름 / 달 지름 = 2.65  -> 개월식 때 달이 본영에 완전히 잠김

# %% [markdown]
# ## 2. 반박 3의 핵심 실험 — "도형은 밤의 본질이 아니다"
#
# 카스텔리니: *"대지가 아무런 그림자도 도형도 만들지 않는다 해도, 단순한 어둠과 빛의 결여만으로 밤일 것이다."*
#
# 이것을 기하로 옮기면: **$R_S$를 바꿔 보라.** 밑면 반지름 $R_E$(=지구의 불투명한 몸)는 그대로인데
# 그림자의 *figura*는 완전히 달라진다.
#
# - $R_S > R_E$ : 수렴하는 원뿔 (conoide, 카스텔리니가 인용한 Bartholomaeus Anglicus의 *umbra conoidem*)
# - $R_S = R_E$ : 무한 원기둥 — 꼭짓점이 없다
# - $R_S < R_E$ : 발산하는 원뿔 — 영원히 닫히지 않는다
#
# 세 경우 모두 **태양 반대편 지표는 여전히 직사광을 못 받는다 = 밤이다.**
# 따라서 "밤"은 도형에 무차별하고, 도형은 밤이라는 결여에 크기·형태의 규정이 덧붙은
# *privatio contracta et restricta*일 뿐이다. → 밤이 그림자의 원인, 역이 아니다.

# %%
print(f"{'R_s / R_E':>10} | {'원뿔 길이 L [km]':>16} | {'도형(figura)':<14} | 태양 반대편은?")
print("-" * 70)
for ratio in (109.2, 10.0, 1.0, 0.5):
    R_s = ratio * R_EARTH
    Lx = umbra_length(R_s=R_s)
    if math.isinf(Lx):
        shape, ltxt = "무한 원기둥", "inf"
    elif Lx > 0:
        shape, ltxt = "수렴 원뿔", f"{Lx:,.0f}"
    else:
        shape, ltxt = "발산 원뿔", f"{Lx:,.0f} (<0)"
    print(f"{ratio:>10.1f} | {ltxt:>16} | {shape:<14} | 밤 (직사광 0)")
# 출력:  R_s / R_E |   원뿔 길이 L [km] | 도형(figura)     | 태양 반대편은?
# 출력: ----------------------------------------------------------------------
# 출력:      109.2 |        1,382,605 | 수렴 원뿔          | 밤 (직사광 0)
# 출력:       10.0 |       16,621,986 | 수렴 원뿔          | 밤 (직사광 0)
# 출력:        1.0 |              inf | 무한 원기둥         | 밤 (직사광 0)
# 출력:        0.5 | -299,195,741 (<0) | 발산 원뿔          | 밤 (직사광 0)
#
# 세 도형이 전부 다르지만 "태양 반대편은 밤"은 한 번도 흔들리지 않는다.
# → figura 는 밤의 essentia 밖에 있다 (카스텔리니 반박 3).

# %% [markdown]
# ## 3. 박명(twilight)은 '그림자의 경계'가 아니다
#
# 밤낮 경계(terminator)를 "그림자의 테두리"로 보면, 그 테두리는 광원이 점광원일 때만 날카롭다.
# 태양은 각반지름 $\rho_\odot = \arcsin(R_S/d) \approx 0.266°$의 **면광원**이므로,
# 지표에서 태양이 부분적으로만 가려지는 띠(= 반영이 지표를 스치는 폭)가 생긴다:
#
# $$w_{\text{geom}} = R_E \cdot 2\rho_\odot$$
#
# 반면 실제 박명 구간은 태양 **고도각** $h$로 정의된다 (civil $-6°$, nautical $-12°$, astronomical $-18°$).
# 지표에서 부분광 띠의 폭과 비교하면:
#
# $$w(h) = R_E \cdot |h|\ (\text{rad})$$
#
# 두 수를 비교하면 박명이 무엇 때문에 생기는지가 드러난다.

# %%
rho_sun = math.degrees(math.asin(R_SUN / AU))
w_geom = R_EARTH * math.radians(2 * rho_sun)
print(f"태양 각반지름 rho = {rho_sun:.4f} deg  (= {rho_sun*60:.2f} arcmin, 알려진 값 약 16')")
print(f"기하학적 부분광(반영) 띠 폭 w_geom = {w_geom:,.0f} km\n")

print(f"{'구간':<26} {'고도각 h':>9} {'터미네이터로부터 폭':>20}")
print("-" * 60)
for name, h in (("geometric penumbra", -2 * rho_sun),
                ("civil twilight", -6.0),
                ("nautical twilight", -12.0),
                ("astronomical twilight", -18.0)):
    print(f"{name:<26} {h:>8.2f}° {R_EARTH*math.radians(abs(h)):>17,.0f} km")
# 출력: 태양 각반지름 rho = 0.2665 deg  (= 15.99 arcmin, 알려진 값 약 16')
# 출력: 기하학적 부분광(반영) 띠 폭 w_geom = 59 km
# 출력:
# 출력: 구간                             고도각 h           터미네이터로부터 폭
# 출력: ------------------------------------------------------------
# 출력: geometric penumbra            -0.53°                59 km
# 출력: civil twilight                -6.00°               667 km
# 출력: nautical twilight            -12.00°             1,334 km
# 출력: astronomical twilight        -18.00°             2,002 km

# %% [markdown]
# ### 이 수치가 말해 주는 것
#
# 순수 기하학적 반영 띠는 **59 km**밖에 안 되는데, 천문박명 경계는 **2,000 km**나 안쪽으로 들어와 있다.
# 즉 우리가 체감하는 "밤이 되는 과정"의 97%는 *그림자 도형*이 아니라
# **대기 산란으로 남은 간접광의 세기**가 결정한다.
#
# 카스텔리니의 언어로 바꾸면:
# - **직사광의 유무**(기하학적 차폐, 태양의 위치와 크기가 정하는 것) = 밤의 본래 규정
# - **그림자의 뾰족한 원뿔 도형** = 여기에 크기·형태가 덧붙은 파생물
# - 실제 어둠의 정도 = "빛이 얼마나 결여됐는가"의 연속 스펙트럼
#
# 셋 다 "밤 = 빛의 결여"를 1차 개념으로, "그림자 도형"을 2차 개념으로 놓았을 때 자연스럽게 정리된다.
# 다만 반박 1과 2에 대해서는 현대 천문학이 카스텔리니에게 절반만 동의한다:
# 밤의 **작용인**은 태양도 대지의 몸도 아니라 **지구의 자전**이고,
# 태양과 대지는 밤의 *조건*(광원과 차폐체)일 뿐이다. 다음 셀에서 그 시간 규모를 확인한다.

# %%
# 카스텔리니에게 없던 요소: 자전. 터미네이터가 지표를 스치는 속도로 박명 지속시간이 나온다.
OMEGA = 2 * math.pi / 86_164.1     # 항성일 기준 자전 각속도 [rad/s]
for name, h in (("geometric penumbra", -2 * rho_sun), ("civil", -6.0),
                ("nautical", -12.0), ("astronomical", -18.0)):
    dt = math.radians(abs(h)) / OMEGA / 60.0   # 적도, 춘분 기준 최소 지속시간 [min]
    print(f"{name:<20} {abs(h):>6.2f}° -> 적도 기준 최소 {dt:>6.1f} min")
# 출력: geometric penumbra     0.53° -> 적도 기준 최소    2.1 min
# 출력: civil                  6.00° -> 적도 기준 최소   23.9 min
# 출력: nautical              12.00° -> 적도 기준 최소   47.9 min
# 출력: astronomical          18.00° -> 적도 기준 최소   71.8 min

# %% [markdown]
# ## 4. 그림 — 본영/반영 원뿔 + 박명 띠
#
# 왼쪽: 지구 중심을 원점, 태양은 $-x$ 방향(1 AU 밖). 본영 원뿔(진한 회색)과 반영 원뿔(연회색),
# 달 거리 단면 표시. 밤은 이 원뿔의 **안쪽**이다.
#
# 오른쪽: 지구 단면. 낮 반구 / 기하학적 반영 띠 / 3단 박명 / 완전한 밤을
# 태양천정거리 기준 각도 쐐기로 나눈다. 경계는 모두 **광원의 기하학적 차폐 각도**로 결정된다.

# %%
import plotly.graph_objects as go
from plotly.subplots import make_subplots

fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=("본영 / 반영 원뿔 (지구 중심 좌표계)",
                    "지구 단면: 터미네이터와 박명 띠"),
    horizontal_spacing=0.11,
)

# ---------- 좌: 원뿔 단면 ----------
X_MAX = 1.55e6
xs = [i * X_MAX / 400 for i in range(401)]

# 반영: 원뿔 바깥 → 위/아래 대칭 영역을 fill 로
pu = [penumbra_radius(x) for x in xs]
uu = [max(umbra_radius(x), 0.0) for x in xs]

fig.add_trace(go.Scatter(
    x=xs + xs[::-1], y=pu + [-v for v in pu[::-1]],
    fill="toself", fillcolor="rgba(255,214,102,0.30)",
    line=dict(color="rgba(214,160,20,0.85)", width=1.2),
    name="반영 (penumbra)", hoverinfo="skip"), row=1, col=1)

fig.add_trace(go.Scatter(
    x=xs + xs[::-1], y=uu + [-v for v in uu[::-1]],
    fill="toself", fillcolor="rgba(38,44,66,0.90)",
    line=dict(color="rgba(38,44,66,1)", width=1.2),
    name="본영 (umbra) = 밤", hoverinfo="skip"), row=1, col=1)

# 지구 (스케일 왜곡이 크므로 세로 막대로 표시)
fig.add_trace(go.Scatter(
    x=[0, 0], y=[-R_EARTH, R_EARTH], mode="lines",
    line=dict(color="#1f77b4", width=7),
    name=f"지구 (R_E={R_EARTH:,.0f} km)"), row=1, col=1)

# 달 거리 단면
fig.add_trace(go.Scatter(
    x=[D_MOON, D_MOON], y=[-rp_moon, rp_moon], mode="lines",
    line=dict(color="#888", width=1, dash="dot"),
    name="달 거리 단면", hoverinfo="skip"), row=1, col=1)
fig.add_trace(go.Scatter(
    x=[D_MOON, D_MOON], y=[ru_moon, rp_moon], mode="markers",
    marker=dict(size=7, symbol="diamond", color="#d62728"),
    name=f"r_u={ru_moon:,.0f} / r_p={rp_moon:,.0f} km"), row=1, col=1)

fig.add_annotation(x=D_MOON, y=rp_moon * 1.18, row=1, col=1, showarrow=False,
                   text=f"달 거리<br>r_u={ru_moon:,.0f} km<br>r_p={rp_moon:,.0f} km",
                   font=dict(size=9))
fig.add_annotation(x=L, y=0, ax=-70, ay=-46, row=1, col=1,
                   text=f"원뿔 꼭짓점<br>L={L/1e6:.3f}×10⁶ km",
                   font=dict(size=9), arrowsize=0.8)
fig.add_annotation(x=0.02 * X_MAX, y=-rp_moon * 2.6, row=1, col=1, showarrow=False,
                   xanchor="left", font=dict(size=9, color="#b45309"),
                   text="← 태양 방향 (1 AU)")

# ---------- 우: 지구 단면 + 박명 쐐기 ----------
def wedge(a0, a1, color, label, n=90):
    """태양 천정 방향을 +x 로 두고, 천정거리 a0~a1 [deg] 사이 쐐기."""
    px, py = [0.0], [0.0]
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        px.append(R_EARTH * math.cos(a))
        py.append(R_EARTH * math.sin(a))
    return go.Scatter(x=px + px[::-1], y=py + [-v for v in py[::-1]],
                      fill="toself", fillcolor=color, line=dict(width=0),
                      name=label, hoverinfo="skip")


bands = [
    (0.0, 90.0, "rgba(255,236,150,0.95)", "낮 (h > 0°)"),
    (90.0, 90.0 + 2 * rho_sun, "rgba(255,170,80,0.95)", f"기하 반영 ({w_geom:,.0f} km)"),
    (90.0 + 2 * rho_sun, 96.0, "rgba(150,150,200,0.80)", "시민박명 (−6°)"),
    (96.0, 102.0, "rgba(90,95,160,0.85)", "항해박명 (−12°)"),
    (102.0, 108.0, "rgba(52,54,110,0.90)", "천문박명 (−18°)"),
    (108.0, 180.0, "rgba(16,18,42,0.97)", "완전한 밤 = privatio lucis"),
]
for a0, a1, c, lab in bands:
    fig.add_trace(wedge(a0, a1, c, lab), row=1, col=2)

# 지구 윤곽 + 터미네이터
circ_x = [R_EARTH * math.cos(2 * math.pi * i / 240) for i in range(241)]
circ_y = [R_EARTH * math.sin(2 * math.pi * i / 240) for i in range(241)]
fig.add_trace(go.Scatter(x=circ_x, y=circ_y, mode="lines",
                         line=dict(color="#1f77b4", width=2),
                         showlegend=False, hoverinfo="skip"), row=1, col=2)
fig.add_trace(go.Scatter(x=[0, 0], y=[-R_EARTH, R_EARTH], mode="lines",
                         line=dict(color="#e11", width=1.5, dash="dash"),
                         name="터미네이터 (h = 0°)"), row=1, col=2)
fig.add_annotation(x=R_EARTH * 0.98, y=R_EARTH * 1.12, row=1, col=2, showarrow=False,
                   text="☀ 태양 천정 방향", font=dict(size=10, color="#b45309"))
fig.add_annotation(x=-R_EARTH * 0.55, y=0, row=1, col=2, showarrow=False,
                   text="밤<br>(빛의 결여)", font=dict(size=11, color="#eee"))

fig.update_xaxes(title_text="지구 중심으로부터의 거리 [km]", row=1, col=1)
fig.update_yaxes(title_text="축으로부터의 반지름 [km]",
                 range=[-rp_moon * 3.2, rp_moon * 3.2], row=1, col=1)
fig.update_xaxes(title_text="km", row=1, col=2)
fig.update_yaxes(title_text="km", scaleanchor="x2", scaleratio=1, row=1, col=2)

fig.update_layout(
    title=dict(text="밤은 '대지의 그림자'가 아니라 '빛의 결여'다 — 카스텔리니 논증의 천문 기하",
               x=0.5, font=dict(size=15)),
    template="plotly_white", width=1280, height=560,
    legend=dict(orientation="h", yanchor="top", y=-0.20, x=0.0, font=dict(size=9)),
    margin=dict(t=90, b=140, l=70, r=30),
)

_show(fig)

import os
_out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expy.png")
fig.write_image(_out, scale=2)
print(f"saved: {_out}")
# 출력: saved: /Users/.../c4d459a3-82cb-4fde-8cec-a141bfa8be28/expy.png
# 참고: 좌측 패널은 x/y 축 스케일이 크게 다르다 (x는 10^6 km, y는 10^4 km).
#       실제 원뿔의 반각은 15.84' 로 극히 뾰족하다.

# %% [markdown]
# ## 5. 정리 — 계산 결과와 카스텔리니의 세 반박
#
# | 카스텔리니 | 기하로 확인된 것 | 현대 천문학과의 차이 |
# |---|---|---|
# | ① 그림자가 아니라 **불투명한 대지의 몸**이 작용인 | 원뿔의 밑면 반지름 = $R_E$. 그림자는 스스로 아무것도 가리지 않는다 | 맞다. 단 '작용인'이라기보다 차폐 *조건* |
# | ② 오히려 **진 태양**이 원인 | $L$, $\rho_\odot$, 반영 기울기 모두 $R_S, d$ 함수 → 도형은 광원이 정한다 | 부분적으로 맞다. 리듬의 진짜 원인은 **지구 자전**(23h56m) |
# | ③ 밤은 그림자의 결과가 아니라 **원인**; 밤은 도형을 본질에 포함하지 않는다 | $R_S$를 바꾸면 원뿔→원기둥→발산뿔로 도형이 뒤집히지만 '직사광 0'은 불변 | 개념적으로 정확. 그림자는 결여에 도형이 한정된 특수 사례 |
#
# 그리고 어원: 카스텔리니가 인용한 *Nox ← nocere*(해치다)는 바로(Varro)·이시도루스 계열의
# **민간어원**이고, 실제로 *nox*는 인도유럽어 어근 $\ast n\acute{o}k^{\!w}ts$(그리스어 νύξ, 산스크리트 nákt,
# 영어 night와 동원)에서 왔다. *noceō*는 $\ast nek\text{-}$('죽음/해')에서 온 별개 어근이다.
# 그러나 그 잘못된 어원이 카스텔리니의 논증을 이끌었다는 점은 흥미롭다 —
# "밤이 시각의 완전성(*perfezione*, 곧 보는 행위)을 **빼앗는다**"는 착상은
# 이미 밤을 **결여(privatio)**로 규정하고 있으며, 그것이 그림자 도형론을 뒤집는 지렛대가 된다.
