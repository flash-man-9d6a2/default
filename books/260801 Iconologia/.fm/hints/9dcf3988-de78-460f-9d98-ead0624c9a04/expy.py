# 필요 패키지: numpy, plotly, kaleido  (pip install numpy plotly kaleido)
# 실행: python3 expy.py  또는 VSCode에서 "# %%" 셀 단위 실행
#
# 주제: 리파 『Iconologia』의 Musica 도상 — "모루(대장간)"와 "저울 속 철제 망치"가
#       가리키는 음악 이론을 수치로 검증한다.
#         1) 현의 길이비 -> 진동수비 -> 협화음(2:1, 3:2, 4:3) 파형 합성
#         2) "망치의 무게가 음높이를 정한다"는 전승의 물리적 검증
#         3) 진동수를 실제로 정하는 양: f = (1/(2L)) * sqrt(T/mu)
#         4) 순정률 vs 평균율 센트 차이 (저울 = 귀의 계량)

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


def cents(ratio):
    """진동수비 -> 센트(1200 * log2(ratio))."""
    return 1200.0 * np.log2(ratio)


print("numpy", np.__version__)
# 출력: numpy 2.0.2

# %% [markdown]
# ## 1. 저울의 논리: 길이비가 곧 진동수비
#
# 팽팽한 현에서 기본 진동수는 길이에 반비례한다.
#
# $$f \propto \frac{1}{L} \quad\Rightarrow\quad \frac{f_2}{f_1} = \frac{L_1}{L_2}$$
#
# 그래서 현을 $1:2$로 나누면 옥타브($2:1$), $2:3$이면 5도($3:2$), $3:4$이면 4도($4:3$)가 된다.
# 리파의 "저울"은 바로 이 **비(ratio)를 귀가 계량한다**는 뜻이다.

# %%
BASE = 220.0  # A3
intervals = [
    ("옥타브 (diapason)", 2, 1),
    ("완전5도 (diapente)", 3, 2),
    ("완전4도 (diatessaron)", 4, 3),
    ("온음 (tono)", 9, 8),
]

print(f"{'음정':22s} {'현 길이비':>10s} {'진동수비':>9s} {'f2(Hz)':>9s} {'센트':>9s}")
for name, p, q in intervals:
    r = p / q
    print(f"{name:22s} {f'{q}:{p}':>10s} {f'{p}:{q}':>9s} {BASE * r:9.2f} {cents(r):9.2f}")
# 출력: 음정                      현 길이비      진동수비    f2(Hz)        센트
# 출력: 옥타브 (diapason)              1:2       2:1    440.00   1200.00
# 출력: 완전5도 (diapente)             2:3       3:2    330.00    701.96
# 출력: 완전4도 (diatessaron)          3:4       4:3    293.33    498.04
# 출력: 온음 (tono)                    8:9       9:8    247.50    203.91

# %% [markdown]
# ### 협화음이 "합성 파형의 주기"로 드러난다
#
# 두 정현파를 더하면 합성 파형의 주기는 두 주기의 최소공배수다.
# 비가 간단한 정수비($2:1$, $3:2$)일수록 주기가 짧게 반복되어 귀에 안정적으로 들린다.

# %%
t = np.linspace(0, 0.03, 3000)  # 30 ms


def blend(p, q, f0=BASE):
    return np.sin(2 * np.pi * f0 * t) + np.sin(2 * np.pi * f0 * (p / q) * t)


# 합성 파형의 반복 주기(초) = q / f0  (p:q가 기약일 때)
for name, p, q in intervals:
    print(f"{name:22s} 합성 주기 = {q / BASE * 1000:6.3f} ms")
# 출력: 옥타브 (diapason)       합성 주기 =  4.545 ms
# 출력: 완전5도 (diapente)      합성 주기 =  9.091 ms
# 출력: 완전4도 (diatessaron)   합성 주기 = 13.636 ms
# 출력: 온음 (tono)             합성 주기 = 36.364 ms

# 불협화 비교: 무리비(√2, 트라이톤 근사)는 주기가 닫히지 않는다
irr = np.sin(2 * np.pi * BASE * t) + np.sin(2 * np.pi * BASE * np.sqrt(2) * t)
print("√2 비(600센트) 합성 파형: 유한 주기 없음 ->", f"{cents(np.sqrt(2)):.2f} 센트")
# 출력: √2 비(600센트) 합성 파형: 유한 주기 없음 -> 600.00 센트

# %% [markdown]
# ## 2. 모루 전승의 검증: 망치 무게는 음높이를 그렇게 정하지 않는다
#
# 보에티우스(『De institutione musica』 I.10, 니코마코스 경유)가 전하는 전승에서
# 대장간 망치의 무게는 $12, 9, 8, 6$이고, **진동수가 무게에 반비례한다**고 가정한다.
#
# $$f \propto \frac{1}{m} \;\Rightarrow\; 12{:}6 = 2{:}1(\text{옥타브}),\; 12{:}8=3{:}2,\; 12{:}9=4{:}3,\; 9{:}8=\text{온음}$$
#
# 그러나 실제 고체가 내는 음높이는 **질량이 아니라 형상(모드)** 이 정한다.
# 같은 재질의 망치머리를 기하학적으로 닮은꼴로 $s$배 키우면
#
# $$L \to sL,\quad m \to s^3 m,\quad f \to \frac{f}{s}
# \quad\Rightarrow\quad f \propto m^{-1/3}$$
#
# 즉 옥타브(진동수 2배)를 얻으려면 무게를 2배가 아니라 **8배** 바꿔야 한다.
# 게다가 대장간에서 들리는 음의 대부분은 망치가 아니라 **모루/피가공물**의 고유 모드다.

# %%
weights = [12, 9, 8, 6]
pairs = [(12, 6), (12, 8), (12, 9), (9, 8)]

print(f"{'무게비':>8s} {'전승 f∝1/m':>14s} {'실제 f∝m^-1/3':>16s} {'오차(센트)':>12s}")
for a, b in pairs:
    legend_c = cents(a / b)
    real_c = cents((a / b) ** (1 / 3))
    print(f"{f'{a}:{b}':>8s} {legend_c:14.2f} {real_c:16.2f} {legend_c - real_c:12.2f}")
# 출력:      무게비      전승 f∝1/m    실제 f∝m^-1/3     오차(센트)
# 출력:     12:6        1200.00           400.00       800.00
# 출력:     12:8         701.96           233.99       467.97
# 출력:     12:9         498.04           166.01       332.03
# 출력:      9:8         203.91            67.97       135.94

# 전승대로 옥타브를 얻으려면 닮은꼴 망치의 무게비는?
print("닮은꼴 가정에서 옥타브에 필요한 무게비 =", 2**3, ": 1")
# 출력: 닮은꼴 가정에서 옥타브에 필요한 무게비 = 8 : 1

# %% [markdown]
# ## 3. 진동수를 실제로 정하는 양 — 멜센 법칙
#
# $$f = \frac{1}{2L}\sqrt{\frac{T}{\mu}}$$
#
# - 길이 $L$: 반으로 줄이면 정확히 옥타브 (+1200센트) — 전승이 맞는 유일한 축
# - 장력 $T$: 2배로 늘려도 $\sqrt{2}$배(+600센트)뿐. 옥타브에는 **4배** 필요
#   (빈첸초 갈릴레이가 추를 매달아 지적한 바로 그 지점 — "무게 2배 = 옥타브"는 틀렸다)
# - 선밀도 $\mu$: 2배면 $1/\sqrt{2}$배(−600센트)

# %%
def f_string(L, T, mu):
    return np.sqrt(T / mu) / (2 * L)


L0, T0, MU0 = 0.65, 700.0, 0.0042  # m, N, kg/m
f0 = f_string(L0, T0, MU0)
print(f"기준 현: L={L0} m, T={T0} N, mu={MU0} kg/m -> f0 = {f0:.2f} Hz")
# 출력: 기준 현: L=0.65 m, T=700.0 N, mu=0.0042 kg/m -> f0 = 314.04 Hz

for label, f in [
    ("길이 1/2", f_string(L0 / 2, T0, MU0)),
    ("장력 2배", f_string(L0, T0 * 2, MU0)),
    ("장력 4배", f_string(L0, T0 * 4, MU0)),
    ("선밀도 2배", f_string(L0, T0, MU0 * 2)),
]:
    print(f"{label:12s} f = {f:8.2f} Hz  ({cents(f / f0):+8.2f} 센트)")
# 출력: 길이 1/2       f =   628.07 Hz  (+1200.00 센트)
# 출력: 장력 2배        f =   444.12 Hz  ( +600.00 센트)
# 출력: 장력 4배        f =   628.07 Hz  (+1200.00 센트)
# 출력: 선밀도 2배       f =   222.06 Hz  ( -600.00 센트)

# %% [markdown]
# ## 4. 저울의 눈금: 순정률 vs 평균율
#
# "귀의 판단으로 음의 정확함을 잰다"는 저울의 뜻을 현대적으로 옮기면
# 정수비(순정률)와 12등분(평균율)의 차이를 센트로 계량하는 일이 된다.
#
# $$\text{평균율}: f_k = f_0 \cdot 2^{k/12},\qquad \text{센트} = 1200\log_2\frac{f}{f_0}$$

# %%
just = [
    ("1도", 1, 1, 0),
    ("단2도", 16, 15, 1),
    ("장2도", 9, 8, 2),
    ("단3도", 6, 5, 3),
    ("장3도", 5, 4, 4),
    ("완전4도", 4, 3, 5),
    ("증4도", 45, 32, 6),
    ("완전5도", 3, 2, 7),
    ("단6도", 8, 5, 8),
    ("장6도", 5, 3, 9),
    ("단7도", 9, 5, 10),
    ("장7도", 15, 8, 11),
    ("옥타브", 2, 1, 12),
]

names, dev = [], []
print(f"{'음정':8s} {'비':>7s} {'순정률(c)':>11s} {'평균율(c)':>10s} {'차이(c)':>9s}")
for name, p, q, k in just:
    jc, ec = cents(p / q), 100.0 * k
    names.append(name)
    dev.append(jc - ec)
    print(f"{name:8s} {f'{p}:{q}':>7s} {jc:11.2f} {ec:10.1f} {jc - ec:+9.2f}")
# 출력: 음정            비    순정률(c)   평균율(c)   차이(c)
# 출력: 1도          1:1        0.00        0.0    +0.00
# 출력: 단2도       16:15      111.73      100.0   +11.73
# 출력: 장2도         9:8      203.91      200.0    +3.91
# 출력: 단3도         6:5      315.64      300.0   +15.64
# 출력: 장3도         5:4      386.31      400.0   -13.69
# 출력: 완전4도       4:3      498.04      500.0    -1.96
# 출력: 증4도       45:32      590.22      600.0    -9.78
# 출력: 완전5도       3:2      701.96      700.0    +1.96
# 출력: 단6도         8:5      813.69      800.0   +13.69
# 출력: 장6도         5:3      884.36      900.0   -15.64
# 출력: 단7도         9:5     1017.60     1000.0   +17.60
# 출력: 장7도        15:8     1088.27     1100.0   -11.73
# 출력: 옥타브        2:1     1200.00     1200.0    +0.00

# 피타고라스 콤마: 완전5도 12번 vs 옥타브 7번
comma = cents((3 / 2) ** 12 / 2**7)
print(f"피타고라스 콤마 = {comma:.2f} 센트")
# 출력: 피타고라스 콤마 = 23.46 센트

# %% [markdown]
# ## 5. 그림 한 장으로 보기
#
# (1) 협화음 합성 파형, (2) 망치 무게 전승 vs 실제 스케일링,
# (3) 장력에 대한 $\sqrt{\;}$ 의존, (4) 순정률−평균율 센트 편차.

# %%
fig = make_subplots(
    rows=2,
    cols=2,
    subplot_titles=(
        "1) 협화음 합성 파형 (기음 220 Hz)",
        "2) 망치 무게 -> 음높이: 전승 vs 실제",
        "3) f = (1/2L)·sqrt(T/mu) — 장력 의존",
        "4) 순정률 - 평균율 (센트)",
    ),
    vertical_spacing=0.16,
    horizontal_spacing=0.09,
)

# (1) 파형
for i, (name, p, q) in enumerate(intervals[:3]):
    fig.add_trace(
        go.Scatter(x=t * 1000, y=blend(p, q) + 3 * i, mode="lines", name=f"{p}:{q} {name}"),
        row=1,
        col=1,
    )
fig.add_trace(
    go.Scatter(x=t * 1000, y=irr + 9, mode="lines", name="√2 (불협화)", line=dict(dash="dot")),
    row=1,
    col=1,
)

# (2) 무게 -> 진동수비
m = np.linspace(6, 24, 200)
fig.add_trace(
    go.Scatter(x=m, y=12 / m, mode="lines", name="전승 f ∝ 1/m", line=dict(color="crimson")),
    row=1,
    col=2,
)
fig.add_trace(
    go.Scatter(
        x=m, y=(12 / m) ** (1 / 3), mode="lines", name="실제 f ∝ m^(-1/3)", line=dict(color="royalblue")
    ),
    row=1,
    col=2,
)
fig.add_trace(
    go.Scatter(
        x=weights,
        y=[12 / w for w in weights],
        mode="markers+text",
        text=[str(w) for w in weights],
        textposition="top center",
        name="보에티우스 망치 12·9·8·6",
        marker=dict(size=9, color="crimson"),
    ),
    row=1,
    col=2,
)

# (3) 장력 의존
Tr = np.linspace(0.5, 4.5, 200)
fig.add_trace(
    go.Scatter(x=Tr, y=np.sqrt(Tr), mode="lines", name="f/f0 = sqrt(T/T0)", line=dict(color="seagreen")),
    row=2,
    col=1,
)
fig.add_trace(
    go.Scatter(
        x=[2, 4],
        y=[np.sqrt(2), 2.0],
        mode="markers+text",
        text=["T×2 → +600c", "T×4 → 옥타브"],
        textposition="top left",
        name="추 무게 2배는 옥타브가 아니다",
        marker=dict(size=10, color="seagreen"),
    ),
    row=2,
    col=1,
)

# (4) 센트 편차
fig.add_trace(
    go.Bar(
        x=names,
        y=dev,
        name="순정률 - 평균율",
        marker=dict(color=["indianred" if d > 0 else "steelblue" for d in dev]),
    ),
    row=2,
    col=2,
)

fig.update_xaxes(title_text="시간 (ms)", row=1, col=1)
fig.update_yaxes(title_text="진폭 (오프셋)", showticklabels=False, row=1, col=1)
fig.update_xaxes(title_text="망치 무게 m (임의 단위)", row=1, col=2)
fig.update_yaxes(title_text="진동수비 f/f(12)", row=1, col=2)
fig.update_xaxes(title_text="장력비 T/T0", row=2, col=1)
fig.update_yaxes(title_text="진동수비 f/f0", row=2, col=1)
fig.update_yaxes(title_text="센트", row=2, col=2)
fig.update_layout(
    title="Musica의 모루와 저울: 무게가 아니라 길이·장력·선밀도가 음높이를 정한다",
    height=900,
    width=1300,
    template="plotly_white",
    legend=dict(orientation="h", y=-0.12),
)

_show(fig)
fig.write_image("expy.png", scale=2)
print("saved expy.png")
# 출력: saved expy.png

# %% [markdown]
# ## 정리
#
# - **모루**: "음악은 대장간에서 왔다"는 전승(리파/오를란디는 아비첸나에게 귀속, 원래는
#   니코마코스-보에티우스의 피타고라스 설화). 무게 $12{:}9{:}8{:}6$이 옥타브·5도·4도·온음을
#   준다는 계산은 $f \propto 1/m$을 전제하지만, 닮은꼴 고체는 $f \propto m^{-1/3}$이어서
#   옥타브에서 800센트나 어긋난다.
# - **저울 속 망치**: 무게를 손이 재듯 음의 정확함(정률)을 귀가 잰다는 유비.
#   현대적으로는 센트 계량, 즉 $1200\log_2(f/f_0)$가 그 저울의 눈금이다.
# - 실제로 음높이를 정하는 것은 무게가 아니라 $f = \frac{1}{2L}\sqrt{T/\mu}$ —
#   길이·장력·선밀도. 전승이 맞는 축은 **길이**뿐이다.
