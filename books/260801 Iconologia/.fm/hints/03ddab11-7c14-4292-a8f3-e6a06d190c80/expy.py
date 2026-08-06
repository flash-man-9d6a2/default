# %% [markdown]
# # 행성시(ore planetali)와 요일 이름의 산술
#
# 리파 『이코놀로지아』의 「낮의 시간 / 밤의 시간」 항목은 24개의 시간 의인상에게
# 각각 하나의 **행성 표지(segno di Pianeta)** 를 들려 준다.
# 그 근거는 본문이 직접 밝힌다 — 고대인은 낮 12시간, 밤 12시간을 나누고
# 각 시간을 일곱 행성 중 하나가 다스린다고 보았다(`ore planetali`).
#
# 그리고 조반니 사크로보스코(Johannes de Sacrobosco)의 말을 인용한다:
#
# > *Philosophi enim Gentiles quemlibet diem septimanae, ab illo Planeta,
# > qui dominatur in prima hora illius diei, denominant.*
# > (이교 철학자들은 한 주의 각 날을 그날 **제1시**를 다스리는 행성의 이름으로 부른다.)
#
# 이 노트북에서 확인할 것:
#
# 1. **칼데아 순서** $C=(\text{토성},\text{목성},\text{화성},\text{태양},\text{금성},\text{수성},\text{달})$ 로
#    24시간에 행성을 차례로 배정하면,
# 2. 하루가 끝난 뒤 다음 날 제1시의 지배성은 $24 \bmod 7 = 3$ 칸 뒤로 건너뛰고,
# 3. 그 3칸 도약을 7번 반복하면 정확히 **일-월-화-수-목-금-토** 요일 순서가 나온다.
# 4. 리파 본문의 순서(1시 태양, 2시 금성, 3시 수성, 4시 달, 5시 토성, 6시 목성, 7시 화성)가
#    칼데아 순서를 **태양에서 시작하도록 회전시킨 것**과 같은지도 검증한다.

# %%
def _show(fig):
    try:
        from IPython import get_ipython
        if get_ipython() is not None:  # VSCode 셀/Jupyter에서만 렌더링
            fig.show()
    except ImportError:
        pass


# 칼데아 순서: 지구에서 본 겉보기 공전(회귀) 주기가 긴 것 → 짧은 것
CHALDEAN = ["토성", "목성", "화성", "태양", "금성", "수성", "달"]
PERIOD_DAYS = {  # 겉보기 회귀 주기(일) — 칼데아 순서의 근거
    "토성": 10759.2, "목성": 4332.6, "화성": 686.98,
    "태양": 365.26, "금성": 224.70, "수성": 87.97, "달": 27.32,
}

print(CHALDEAN)
print([PERIOD_DAYS[p] for p in CHALDEAN])
print("주기 내림차순인가?", [PERIOD_DAYS[p] for p in CHALDEAN] == sorted(PERIOD_DAYS.values(), reverse=True))
# 출력: ['토성', '목성', '화성', '태양', '금성', '수성', '달']
# 출력: [10759.2, 4332.6, 686.98, 365.26, 224.7, 87.97, 27.32]
# 출력: 주기 내림차순인가? True

# %% [markdown]
# ## 1단계 — 24시간 행성 배정표
#
# 제1시의 지배성을 $s$(칼데아 순서에서의 인덱스)라 하면, 제 $h$ 시의 지배성은
#
# $$P(h) = C\big[(s + h - 1) \bmod 7\big], \qquad h = 1,\dots,24$$
#
# 리파는 "논증을 위해 낮 제1시를 태양으로 시작한다"고 명시하므로 $s = C^{-1}(\text{태양}) = 3$.

# %%
def hour_ruler(start_planet: str, h: int) -> str:
    """제1시 지배성이 start_planet일 때 제h시(1-based)의 지배 행성."""
    s = CHALDEAN.index(start_planet)
    return CHALDEAN[(s + h - 1) % 7]


ripa_day = [hour_ruler("태양", h) for h in range(1, 25)]
for h in range(1, 25):
    tag = f"낮 {h:2d}시" if h <= 12 else f"밤 {h - 12:2d}시"
    print(f"h={h:2d}  {tag}  →  {ripa_day[h - 1]}")
# 출력: h= 1  낮  1시  →  태양
# 출력: h= 2  낮  2시  →  금성
# 출력: h= 3  낮  3시  →  수성
# 출력: h= 4  낮  4시  →  달
# 출력: h= 5  낮  5시  →  토성
# 출력: h= 6  낮  6시  →  목성
# 출력: h= 7  낮  7시  →  화성
# 출력: h= 8  낮  8시  →  태양
# 출력: h= 9  낮  9시  →  금성
# 출력: h=10  낮 10시  →  수성
# 출력: h=11  낮 11시  →  달
# 출력: h=12  낮 12시  →  토성
# 출력: h=13  밤  1시  →  목성
# 출력: h=14  밤  2시  →  화성
# 출력: h=15  밤  3시  →  태양
# 출력: h=16  밤  4시  →  금성
# 출력: h=17  밤  5시  →  수성
# 출력: h=18  밤  6시  →  달
# 출력: h=19  밤  7시  →  토성
# 출력: h=20  밤  8시  →  목성
# 출력: h=21  밤  9시  →  화성
# 출력: h=22  밤 10시  →  태양
# 출력: h=23  밤 11시  →  금성
# 출력: h=24  밤 12시  →  수성

# %% [markdown]
# ## 2단계 — 리파 본문과 대조
#
# 실제 『이코놀로지아』 제4권 본문에서 각 시간의 의인상이 손에 든 행성 표지를 옮겨 적으면
# 위 계산과 완전히 일치해야 한다. 낮 12시간, 밤 12시간을 그대로 읽어 넣는다.

# %%
RIPA_TEXT = [
    # 낮의 시간 (ORE DEL GIORNO) 1~12
    "태양", "금성", "수성", "달", "토성", "목성", "화성", "태양", "금성", "수성", "달", "토성",
    # 밤의 시간 (ORE DELLA NOTTE) 1~12
    "목성", "화성", "태양", "금성", "수성", "달", "토성", "목성", "화성", "태양", "금성", "수성",
]

print("리파 본문과 칼데아 계산이 일치?", RIPA_TEXT == ripa_day)
mismatch = [(h + 1, RIPA_TEXT[h], ripa_day[h]) for h in range(24) if RIPA_TEXT[h] != ripa_day[h]]
print("불일치:", mismatch)

# 리파의 앞 7시간 = 칼데아 순서를 '태양'에서 시작하도록 회전시킨 것인가?
rotated = CHALDEAN[CHALDEAN.index("태양"):] + CHALDEAN[:CHALDEAN.index("태양")]
print("리파 1~7시   :", RIPA_TEXT[:7])
print("칼데아 회전본:", rotated)
print("동일?", RIPA_TEXT[:7] == rotated)
print("참고) 칼데아 순서를 '뒤집은' 것과는 다름:", list(reversed(CHALDEAN)))
# 출력: 리파 본문과 칼데아 계산이 일치? True
# 출력: 불일치: []
# 출력: 리파 1~7시   : ['태양', '금성', '수성', '달', '토성', '목성', '화성']
# 출력: 칼데아 회전본: ['태양', '금성', '수성', '달', '토성', '목성', '화성']
# 출력: 동일? True
# 출력: 참고) 칼데아 순서를 '뒤집은' 것과는 다름: ['달', '수성', '금성', '태양', '화성', '목성', '토성']

# %% [markdown]
# ## 3단계 — 핵심 산술: $24 \bmod 7 = 3$
#
# 하루가 24시간이고 행성은 7개이므로, 하루가 끝나면 순환은 제자리로 돌아오지 못하고
# **3칸** 어긋난 채 다음 날이 시작된다.
#
# $$24 = 3\cdot 7 + 3 \quad\Longrightarrow\quad 24 \equiv 3 \pmod 7$$
#
# 즉 오늘 제1시 지배성이 $C[s]$ 이면 내일 제1시 지배성은 $C[(s+3) \bmod 7]$ 이다.
# 사크로보스코의 규칙("그날 제1시를 다스리는 행성이 그날의 이름")을 적용하면
# 요일 이름의 순서는 칼데아 원 위에서 **세 칸씩 건너뛴 궤적**이 된다.

# %%
print("24 // 7 =", 24 // 7, " / 24 % 7 =", 24 % 7)

WEEKDAY_OF = {  # 지배 행성 → 요일 (라틴·로망스어 요일명의 어원)
    "태양": "일요일 (dies Solis)",
    "달": "월요일 (dies Lunae)",
    "화성": "화요일 (dies Martis)",
    "수성": "수요일 (dies Mercurii)",
    "목성": "목요일 (dies Iovis)",
    "금성": "금요일 (dies Veneris)",
    "토성": "토요일 (dies Saturni)",
}

s = CHALDEAN.index("태양")   # 리파처럼 태양(일요일)에서 출발
first_hour_rulers = []
for d in range(7):
    p = CHALDEAN[(s + 3 * d) % 7]
    first_hour_rulers.append(p)
    print(f"{d + 1}일째: 제1시 지배성 = {p:3s} → {WEEKDAY_OF[p]}")
# 출력: 24 // 7 = 3  / 24 % 7 = 3
# 출력: 1일째: 제1시 지배성 = 태양  → 일요일 (dies Solis)
# 출력: 2일째: 제1시 지배성 = 달   → 월요일 (dies Lunae)
# 출력: 3일째: 제1시 지배성 = 화성  → 화요일 (dies Martis)
# 출력: 4일째: 제1시 지배성 = 수성  → 수요일 (dies Mercurii)
# 출력: 5일째: 제1시 지배성 = 목성  → 목요일 (dies Iovis)
# 출력: 6일째: 제1시 지배성 = 금성  → 금요일 (dies Veneris)
# 출력: 7일째: 제1시 지배성 = 토성  → 토요일 (dies Saturni)

# %%
# 3칸 도약을 '가정'하지 말고, 168시간(=7일)을 실제로 한 칸씩 돌려서 재확인
stream = [CHALDEAN[(s + i) % 7] for i in range(7 * 24)]
derived = [stream[24 * d] for d in range(7)]
print("168시간 순환에서 뽑은 각 날 제1시:", derived)
print("3칸 도약 공식과 일치?", derived == first_hour_rulers)
print("8일째 제1시(=169번째 시간):", CHALDEAN[(s + 7 * 24) % 7], "→ 한 주 뒤 원위치")
# 출력: 168시간 순환에서 뽑은 각 날 제1시: ['태양', '달', '화성', '수성', '목성', '금성', '토성']
# 출력: 3칸 도약 공식과 일치? True
# 출력: 8일째 제1시(=169번째 시간): 태양 → 한 주 뒤 원위치
# 참고: 7*24=168, 168 % 7 == 0 이므로 7일 뒤 정확히 복귀한다.

# %% [markdown]
# ## 4단계 — 칠각별(heptagram) 시각화
#
# 칼데아 순서 7행성을 원 위에 시계방향으로 배치하고, 각 점에서 **3칸 건너뛴** 점으로 선을 그으면
# 한붓그리기로 별 모양 $\{7/3\}$ 칠각별이 만들어진다.
# 이 별을 따라간 궤적이 곧 요일 순서다.
#
# $\gcd(3,7)=1$ 이므로 7개 꼭짓점을 하나도 빠짐없이 지나 원점으로 돌아온다.
# (만약 하루가 21시간이었다면 $21 \bmod 7 = 0$ 이라 매일 같은 행성이 지배해 요일 이름이 생기지 않는다.)

# %%
import math

import plotly.graph_objects as go
from plotly.subplots import make_subplots

SYMBOL = {"토성": "♄", "목성": "♃", "화성": "♂", "태양": "☉", "금성": "♀", "수성": "☿", "달": "☾"}
KOR_DAY = {"태양": "일", "달": "월", "화성": "화", "수성": "수", "목성": "목", "금성": "금", "토성": "토"}

# 원 위 좌표: 칼데아 순서를 12시 방향부터 시계방향으로
pos = {}
for i, p in enumerate(CHALDEAN):
    ang = math.pi / 2 - 2 * math.pi * i / 7
    pos[p] = (math.cos(ang), math.sin(ang))

fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=("칠각별 {7/3}: 3칸 도약 = 요일 순서", "24시간 행성시 배정 (리파 본문과 일치)"),
    column_widths=[0.42, 0.58],
    specs=[[{"type": "xy"}, {"type": "xy"}]],
)

# --- 왼쪽: 칠각별 ---
# 바깥 원(칼데아 순서, 이웃끼리 = 시간의 진행)
circ = [pos[CHALDEAN[i % 7]] for i in range(8)]
fig.add_trace(go.Scatter(
    x=[c[0] for c in circ], y=[c[1] for c in circ], mode="lines",
    line=dict(color="rgba(120,120,120,0.45)", width=1.5, dash="dot"),
    name="칼데아 순서 (시간마다 1칸)", hoverinfo="skip",
), row=1, col=1)

# 별(3칸 도약, 하루마다)
star = []
idx = CHALDEAN.index("태양")
for _ in range(8):
    star.append(pos[CHALDEAN[idx % 7]])
    idx += 3
fig.add_trace(go.Scatter(
    x=[c[0] for c in star], y=[c[1] for c in star], mode="lines",
    line=dict(color="#c1121f", width=2.6),
    name="3칸 도약 (하루마다) = 요일", hoverinfo="skip",
), row=1, col=1)

order_no = {p: i + 1 for i, p in enumerate(first_hour_rulers)}
fig.add_trace(go.Scatter(
    x=[pos[p][0] for p in CHALDEAN], y=[pos[p][1] for p in CHALDEAN],
    mode="markers+text",
    marker=dict(size=34, color="#fdf0d5", line=dict(color="#003049", width=2)),
    text=[f"{SYMBOL[p]}<br><span style='font-size:10px'>{KOR_DAY[p]}{order_no[p]}</span>" for p in CHALDEAN],
    textposition="middle center", textfont=dict(size=17, color="#003049"),
    hovertext=[f"{p} · {WEEKDAY_OF[p]}" for p in CHALDEAN], hoverinfo="text",
    showlegend=False,
), row=1, col=1)

for p in CHALDEAN:
    x, y = pos[p]
    fig.add_annotation(x=x * 1.32, y=y * 1.32, text=p, showarrow=False,
                       font=dict(size=12, color="#555"), row=1, col=1)

# --- 오른쪽: 24시간 배정 히트맵풍 스캐터 ---
pidx = {p: i for i, p in enumerate(CHALDEAN)}
colors = {"토성": "#4a4e69", "목성": "#8f5d2b", "화성": "#c1121f",
          "태양": "#e8a33d", "금성": "#4c956c", "수성": "#3d5a80", "달": "#9a8c98"}
fig.add_trace(go.Scatter(
    x=list(range(1, 25)), y=[pidx[p] for p in ripa_day],
    mode="lines+markers+text",
    line=dict(color="rgba(0,48,73,0.35)", width=1.5),
    marker=dict(size=17, color=[colors[p] for p in ripa_day]),
    text=[SYMBOL[p] for p in ripa_day], textposition="top center", textfont=dict(size=13),
    hovertext=[f"{'낮' if h <= 12 else '밤'} {((h - 1) % 12) + 1}시 · {ripa_day[h - 1]}" for h in range(1, 25)],
    hoverinfo="text", showlegend=False,
), row=1, col=2)

fig.add_vrect(x0=0.5, x1=12.5, fillcolor="#ffd60a", opacity=0.10, line_width=0, row=1, col=2)
fig.add_vrect(x0=12.5, x1=24.5, fillcolor="#003049", opacity=0.10, line_width=0, row=1, col=2)
fig.add_annotation(x=6.5, y=6.75, text="낮 12시간", showarrow=False, font=dict(size=12), row=1, col=2)
fig.add_annotation(x=18.5, y=6.75, text="밤 12시간", showarrow=False, font=dict(size=12), row=1, col=2)
fig.add_annotation(x=24.9, y=pidx["수성"], ax=40, ay=0, xref="x2", yref="y2",
                   text="25번째 시간 → ☾ 달<br>(다음 날 = 월요일)", showarrow=True,
                   arrowhead=2, font=dict(size=11, color="#c1121f"), arrowcolor="#c1121f")

fig.update_xaxes(title_text="", showticklabels=False, zeroline=False,
                 range=[-1.55, 1.55], row=1, col=1)
fig.update_yaxes(showticklabels=False, zeroline=False, range=[-1.55, 1.55],
                 scaleanchor="x", scaleratio=1, row=1, col=1)
fig.update_xaxes(title_text="하루의 시간 (1~24)", dtick=1, range=[0.2, 26.5], row=1, col=2)
fig.update_yaxes(tickmode="array", tickvals=list(range(7)),
                 ticktext=[f"{SYMBOL[p]} {p}" for p in CHALDEAN],
                 range=[-0.8, 7.2], row=1, col=2)

fig.update_layout(
    title=dict(text="행성시(ore planetali): 24 mod 7 = 3 이 요일 이름을 만든다", x=0.5, font=dict(size=19)),
    template="plotly_white", width=1250, height=560,
    legend=dict(orientation="h", x=0.0, y=-0.13, font=dict(size=11)),
    margin=dict(l=60, r=150, t=90, b=80),
)

_show(fig)
fig.write_image("expy.png", scale=2)
print("expy.png 저장 완료")
# 출력: expy.png 저장 완료
# 필요 패키지: plotly, kaleido (pip install plotly kaleido)

# %% [markdown]
# ## 정리
#
# | 관찰 | 결과 |
# |---|---|
# | 리파가 각 시간에 행성 표지를 들린 이유 | 그 시간이 `ora planetale`, 곧 그 행성이 다스리는 시간이기 때문 |
# | 리파 낮 1~7시 순서 | 태양 → 금성 → 수성 → 달 → 토성 → 목성 → 화성 |
# | 그 정체 | 칼데아 순서(토·목·화·태·금·수·달)를 **태양에서 시작하도록 회전**시킨 것 (역순이 아님) |
# | 24시간 뒤 | $24 \bmod 7 = 3$ → 제1시 지배성이 3칸 도약 |
# | 3칸 도약 7회 | 일·월·화·수·목·금·토 — 사크로보스코가 말한 요일 이름의 유래 |
# | 리파의 하루 | 제1시가 태양 → 이 하루는 **일요일**, 25번째 시간은 달 → 다음 날은 **월요일** |
