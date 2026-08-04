# 필요 패키지: plotly, kaleido  (pip install plotly kaleido)
# 실행: python3 expy.py  또는 VSCode에서 셀 단위 실행 (# %%)

# %% [markdown]
# # 리파 '기계학' 도상의 다섯 도구를 숫자로 확인하기
#
# 리파(Cesare Ripa)의 *Mecanica* 도상은 머리 위에 **원(circolo)** 을 얹고,
# 손과 발밑에 다섯 도구를 배치한다.
#
# | 도상 요소 | 이탈리아어 | 원문이 말하는 성질 |
# |---|---|---|
# | 원 | circolo | 기계적 작동은 대부분 **원운동**에서 나온다 |
# | 지렛대 | manuella | **길이에 비례**해 원운동으로 무게를 든다 (아리스토텔레스 『기계학』) |
# | 도르래 | taglia | **수평·수직** 모두로 큰 무게를 끌고 올린다 |
# | 나사 | vite | **더 쉽게** 원운동으로 들어 올리고 **조인다** |
# | 쐐기 | cuneo | **타격**으로 단단한 것을 쪼갠다 |
# | 권양기 | argano | 중심 아래 원운동으로 **초자연적 무게**를 끈다 |
#
# 이 스크립트의 목표는 두 가지다.
#
# 1. 다섯 도구의 **역학적 이득(mechanical advantage, MA)** 을 각각 계산해 비교한다.
# 2. 이득이 커질수록 **끌어야 하는 거리**가 정확히 그만큼 늘어난다는 것,
#    즉 $F \cdot s = \text{const}$ (일 보존)을 수치로 확인한다.
#
# 원리는 하나다. 반지름 $R$ 과 $r$ 위의 두 점은 같은 각도 $\theta$ 를 돌지만
# 지나는 거리가 다르므로
#
# $$F_{\text{입력}}\,R\theta = F_{\text{하중}}\,r\theta
# \quad\Longrightarrow\quad
# MA = \frac{F_{\text{하중}}}{F_{\text{입력}}} = \frac{R}{r}$$
#
# 머리 위의 원이 뜻하는 것이 바로 이 식이다.

# %%
import math

import plotly.graph_objects as go
from plotly.subplots import make_subplots


def _show(fig):
    try:
        from IPython import get_ipython

        if get_ipython() is not None:  # VSCode 셀/Jupyter에서만 렌더링
            fig.show()
    except ImportError:
        pass


G = 9.80665  # m/s^2
LOAD_MASS = 1000.0  # kg — 다섯 기계가 공통으로 들어야 할 하중
LOAD_FORCE = LOAD_MASS * G  # N
LIFT_HEIGHT = 0.10  # m — 하중을 들어 올릴 높이 (10 cm)

print(f"하중 {LOAD_MASS:.0f} kg = {LOAD_FORCE:,.1f} N")
print(f"들어 올릴 높이 = {LIFT_HEIGHT * 100:.0f} cm")
print(f"필요한 일 W = F·h = {LOAD_FORCE * LIFT_HEIGHT:,.1f} J")
# 출력: 하중 1000 kg = 9,806.6 N
# 출력: 들어 올릴 높이 = 10 cm
# 출력: 필요한 일 W = F·h = 980.7 J

# %% [markdown]
# ## 1. 도구별 MA 공식
#
# 원문의 표현을 그대로 공식에 대응시킨다.
#
# | 도구 | 리파의 표현 | MA |
# |---|---|---|
# | 지렛대 manuella | "그 길이에 따라" | $MA = L_{\text{힘}} / L_{\text{하중}}$ |
# | 도르래 taglia | "수평·수직으로 끈다" | $MA = n$ (하중을 지지하는 줄 개수) |
# | 나사 vite | "더 쉽게" | $MA = 2\pi r / p$ |
# | 쐐기 cuneo | "타격으로 쪼갠다" | $MA = L / t$ |
# | 권양기 argano | "중심 아래 원운동" | $MA = R_{\text{손잡이}} / r_{\text{드럼}}$ |
#
# 지렛대·나사·권양기는 모두 $R/r$ 꼴이다 — 같은 원 원리의 변형일 뿐이다.


# %%
def ma_lever(arm_force_m, arm_load_m):
    """지렛대: 받침점에서 힘점까지 / 하중점까지의 길이 비."""
    return arm_force_m / arm_load_m


def ma_pulley(n_supporting_ropes):
    """도르래(활차 블록): 하중을 지지하는 줄의 개수."""
    return float(n_supporting_ropes)


def ma_screw(handle_radius_m, pitch_m):
    """나사: 손잡이 한 바퀴 원주 / 나사 피치."""
    return 2 * math.pi * handle_radius_m / pitch_m


def ma_wedge(length_m, back_thickness_m):
    """쐐기: 쐐기 길이 / 뒷면(타격면) 두께."""
    return length_m / back_thickness_m


def ma_capstan(handle_radius_m, drum_radius_m):
    """권양기: 손잡이 막대 반지름 / 밧줄이 감기는 드럼 반지름."""
    return handle_radius_m / drum_radius_m


# 리파 판화에 그려진 정도의 현실적인 치수로 설정
MACHINES = [
    # (한글 이름, 이탈리아어, MA, 파라미터 설명)
    ("지렛대", "manuella", ma_lever(1.80, 0.20), "팔 1.80 m : 0.20 m"),
    ("도르래", "taglia", ma_pulley(4), "지지 줄 4개"),
    ("나사", "vite", ma_screw(0.25, 0.006), "손잡이 r=25 cm, 피치 6 mm"),
    ("쐐기", "cuneo", ma_wedge(0.24, 0.030), "길이 24 cm, 두께 3 cm"),
    ("권양기", "argano", ma_capstan(1.50, 0.09), "손잡이 R=1.5 m, 드럼 r=9 cm"),
]

for name, ital, ma, desc in MACHINES:
    print(f"{name:5s} ({ital:9s}) MA = {ma:8.2f}   [{desc}]")
# 출력: 지렛대  (manuella ) MA =     9.00   [팔 1.80 m : 0.20 m]
# 출력: 도르래  (taglia   ) MA =     4.00   [지지 줄 4개]
# 출력: 나사   (vite     ) MA =   261.80   [손잡이 r=25 cm, 피치 6 mm]
# 출력: 쐐기   (cuneo    ) MA =     8.00   [길이 24 cm, 두께 3 cm]
# 출력: 권양기  (argano   ) MA =    16.67   [손잡이 R=1.5 m, 드럼 r=9 cm]

# %% [markdown]
# 벌써 리파의 서술과 일치하는 점이 보인다.
#
# - **나사가 압도적으로 크다** → "앞선 도구들보다 **더 쉽게**(con maggior facilità)".
# - **권양기가 지렛대·도르래보다 크다** → "**초자연적** 무게(pesi soprannaturali)".
#   더구나 권양기는 손잡이 막대에 여러 사람이 붙을 수 있어 실효 출력이 더 커진다.
# - 쐐기의 MA는 다른 것과 성격이 다르다. 쐐기는 무게를 **드는** 게 아니라
#   **쪼개는** 도구여서, 여기서의 MA는 "타격 방향 힘 → 옆으로 벌리는 힘"의 배수다.

# %% [markdown]
# ## 2. 같은 1000 kg을 들 때: 필요한 힘과 끌어야 하는 거리
#
# 마찰이 없다면 일은 보존된다.
#
# $$F_{\text{입력}} \cdot s_{\text{입력}} = F_{\text{하중}} \cdot h$$
#
# 따라서 힘이 $MA$ 배 줄어들면 **움직여야 하는 거리는 정확히 $MA$ 배 늘어난다**.
# 기계는 일을 만들어 주지 않는다. 힘과 거리를 **교환**해 줄 뿐이다.

# %%
print(f"{'도구':<7}{'MA':>9}{'필요 힘(N)':>13}{'≈사람 kgf':>12}{'끌 거리(m)':>13}{'일(J)':>10}")
print("-" * 66)
rows = []
for name, ital, ma, desc in MACHINES:
    f_in = LOAD_FORCE / ma  # 필요한 입력 힘 [N]
    s_in = LIFT_HEIGHT * ma  # 끌어야 하는 거리 [m]
    work = f_in * s_in  # 입력 일 [J] — 항상 같아야 한다
    rows.append((name, ital, ma, f_in, s_in, work))
    print(f"{name:<7}{ma:>9.2f}{f_in:>13.1f}{f_in / G:>12.1f}{s_in:>13.2f}{work:>10.1f}")
# 출력: 도구           MA    필요 힘(N)   ≈사람 kgf   끌 거리(m)     일(J)
# 출력: ------------------------------------------------------------------
# 출력: 지렛대         9.00       1089.6        111.1         0.90     980.7
# 출력: 도르래         4.00       2451.7        250.0         0.40     980.7
# 출력: 나사         261.80         37.5          3.8        26.18     980.7
# 출력: 쐐기           8.00       1225.8        125.0         0.80     980.7
# 출력: 권양기        16.67        588.4         60.0         1.67     980.7

# %%
# 일이 모두 같은지 확인 — 이것이 '원운동 하나의 원리'가 보증하는 것
works = [r[5] for r in rows]
print("입력 일(J):", [round(w, 1) for w in works])
print("모두 동일한가?:", max(works) - min(works) < 1e-9)
print(f"하중이 얻는 일: {LOAD_FORCE * LIFT_HEIGHT:.1f} J")
# 출력: 입력 일(J): [980.7, 980.7, 980.7, 980.7, 980.7]
# 출력: 모두 동일한가?: True
# 출력: 하중이 얻는 일: 980.7 J

# %% [markdown]
# 나사를 보라. 필요한 힘은 **3.8 kgf** — 아이도 돌릴 수 있다.
# 대신 손잡이를 **26.18 m**나 끌어야 한다(반지름 25 cm 손잡이로 약 16.7바퀴).
# 리파가 나사를 "더 쉽다"고 한 것은 **힘**의 이야기이고,
# 그 대가는 **원운동을 그만큼 많이 반복해야 한다**는 것이다.
# 머리 위의 원은 이 '반복되는 회전'의 표지이기도 하다.

# %% [markdown]
# ## 3. 나사를 몇 바퀴 돌려야 하나 (원운동 횟수로 환산)

# %%
screw_r, screw_p = 0.25, 0.006
turns = LIFT_HEIGHT / screw_p
capstan_R, capstan_r = 1.50, 0.09
capstan_turns = (LIFT_HEIGHT * ma_capstan(capstan_R, capstan_r)) / (2 * math.pi * capstan_R)
print(f"나사: 10 cm 올리려면 {turns:.1f} 바퀴, 손이 지나는 거리 {turns * 2 * math.pi * screw_r:.2f} m")
print(f"권양기: 10 cm 끌려면 {capstan_turns:.2f} 바퀴 (사람이 원둘레 {2 * math.pi * capstan_R:.2f} m를 도는 셈)")
# 출력: 나사: 10 cm 올리려면 16.7 바퀴, 손이 지나는 거리 26.18 m
# 출력: 권양기: 10 cm 끌려면 0.18 바퀴 (사람이 원둘레 9.42 m를 도는 셈)

# %% [markdown]
# ## 4. 파라미터에 따른 MA 곡선
#
# 각 도구의 MA가 어떤 치수에 어떻게 반응하는지 본다.
# 지렛대·권양기는 **비($R/r$)에 선형**, 나사는 **피치에 반비례**,
# 도르래는 **정수 계단**, 쐐기는 **두께에 반비례**다.

# %%
fig = make_subplots(
    rows=2,
    cols=3,
    subplot_titles=(
        "지렛대 manuella: 팔 길이비",
        "도르래 taglia: 지지 줄 수",
        "나사 vite: 피치",
        "쐐기 cuneo: 뒷면 두께",
        "권양기 argano: 손잡이 반지름",
        "MA vs 필요 힘 / 끌 거리",
    ),
    specs=[[{}, {}, {}], [{}, {}, {"secondary_y": True}]],
)

# (1) 지렛대: 힘팔 0.2~3.0 m, 하중팔 0.2 m 고정
lf = [0.2 + 0.05 * i for i in range(57)]
fig.add_trace(
    go.Scatter(x=lf, y=[ma_lever(x, 0.20) for x in lf], mode="lines", name="지렛대", line=dict(color="#2E7D32")),
    row=1,
    col=1,
)

# (2) 도르래: 지지 줄 1~8개 (정수만 의미 있음)
ns = list(range(1, 9))
fig.add_trace(
    go.Bar(x=ns, y=[ma_pulley(n) for n in ns], name="도르래", marker_color="#1565C0"),
    row=1,
    col=2,
)

# (3) 나사: 피치 1~20 mm, 손잡이 r=25 cm
ps = [0.001 + 0.0005 * i for i in range(39)]
fig.add_trace(
    go.Scatter(
        x=[p * 1000 for p in ps],
        y=[ma_screw(0.25, p) for p in ps],
        mode="lines",
        name="나사",
        line=dict(color="#C62828"),
    ),
    row=1,
    col=3,
)

# (4) 쐐기: 길이 24 cm 고정, 뒷면 두께 1~8 cm
ts = [0.01 + 0.0025 * i for i in range(29)]
fig.add_trace(
    go.Scatter(
        x=[t * 100 for t in ts],
        y=[ma_wedge(0.24, t) for t in ts],
        mode="lines",
        name="쐐기",
        line=dict(color="#6A1B9A"),
    ),
    row=2,
    col=1,
)

# (5) 권양기: 드럼 r=9 cm 고정, 손잡이 R 0.3~3.0 m
Rs = [0.3 + 0.05 * i for i in range(55)]
fig.add_trace(
    go.Scatter(
        x=Rs, y=[ma_capstan(R, 0.09) for R in Rs], mode="lines", name="권양기", line=dict(color="#EF6C00")
    ),
    row=2,
    col=2,
)

# (6) 일 보존: MA에 대한 필요 힘(감소)과 끌 거리(증가)
ma_axis = [1 + 0.5 * i for i in range(600)]  # MA 1~300.5
fig.add_trace(
    go.Scatter(
        x=ma_axis, y=[LOAD_FORCE / m for m in ma_axis], mode="lines", name="필요 힘 (N)", line=dict(color="#0277BD")
    ),
    row=2,
    col=3,
    secondary_y=False,
)
fig.add_trace(
    go.Scatter(
        x=ma_axis,
        y=[LIFT_HEIGHT * m for m in ma_axis],
        mode="lines",
        name="끌 거리 (m)",
        line=dict(color="#D84315", dash="dash"),
    ),
    row=2,
    col=3,
    secondary_y=True,
)
# 실제 다섯 도구의 위치를 점으로 표시
fig.add_trace(
    go.Scatter(
        x=[r[2] for r in rows],
        y=[r[3] for r in rows],
        mode="markers+text",
        text=[r[0] for r in rows],
        # 점이 겹치지 않도록 도구별로 라벨 위치를 다르게 (지렛대·도르래·나사·쐐기·권양기 순)
        textposition=["top right", "top right", "top left", "bottom left", "bottom right"],
        name="5 도구",
        marker=dict(size=10, color="#212121", symbol="diamond"),
    ),
    row=2,
    col=3,
    secondary_y=False,
)

fig.update_xaxes(title_text="힘팔 길이 (m)", row=1, col=1)
fig.update_xaxes(title_text="줄 개수 n", row=1, col=2)
fig.update_xaxes(title_text="피치 (mm)", row=1, col=3)
fig.update_xaxes(title_text="뒷면 두께 (cm)", row=2, col=1)
fig.update_xaxes(title_text="손잡이 반지름 R (m)", row=2, col=2)
fig.update_xaxes(title_text="MA (log)", type="log", row=2, col=3)
fig.update_yaxes(title_text="MA", row=1, col=1)
fig.update_yaxes(title_text="MA", row=1, col=2)
fig.update_yaxes(title_text="MA", row=1, col=3)
fig.update_yaxes(title_text="MA", row=2, col=1)
fig.update_yaxes(title_text="MA", row=2, col=2)
fig.update_yaxes(title_text="필요 힘 (N)", type="log", row=2, col=3, secondary_y=False)
fig.update_yaxes(title_text="끌 거리 (m)", type="log", row=2, col=3, secondary_y=True)
fig.update_layout(
    title_text="리파 '기계학'의 다섯 도구 — 역학적 이득(MA)과 힘·거리의 교환 (하중 1000 kg, 10 cm 상승)",
    height=760,
    width=1300,
    showlegend=False,
    template="plotly_white",
)

_show(fig)
fig.write_image("expy.png", scale=2)
print("expy.png 저장 완료")
# 출력: expy.png 저장 완료

# %% [markdown]
# ## 5. 정리
#
# - 지렛대·나사·권양기의 MA는 모두 $R/r$ 형태다. 리파가 머리 위에 **원** 을 얹은 이유가
#   여기 있다 — 세 도구는 서로 다른 기계가 아니라 **같은 원 원리의 세 변형**이다.
# - 도르래는 줄의 개수라는 **정수 계단**으로 이득을 얻고, 동시에 힘의 **방향**을 바꾼다
#   ("수평으로도 수직으로도").
# - 쐐기만 원운동이 아니고, 이득도 "든다"가 아니라 "**쪼갠다**"에 쓰인다
#   ("타격을 받아 단단한 것을 나눈다").
# - 어떤 도구를 써도 **일은 980.7 J로 같다**. 기계는 일을 만들지 않고 힘과 거리를 바꾼다.
#   "초자연적 무게(pesi soprannaturali)"라는 리파의 감탄은 힘의 이야기지,
#   에너지의 이야기가 아니다.
