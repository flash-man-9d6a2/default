# %% [markdown]
# # 오를란디의 "3분의 1 가산"은 연이율 몇 %인가
#
# 필요 패키지: `plotly`, `kaleido` (`pip install plotly kaleido`)
#
# 카드 원문(오를란디, *Iconologia* MERCATURA 항목):
#
# > 상인은 거리낌 없이 채무자의 계정에 마땅한 값보다 **아마 3분의 1을 더** 적어 넣는다.
# > 실제로는 현금을 손에 들고 온 사람에게는 선선히 내주었을 값인데도.
#
# 그러면서 오를란디는 두 가지를 동시에 말한다.
#
# 1. 돈을 놀려 두지 않는 상인이 **놓친 이익**(*lucrum cessans*)을 계산해 넣는 것은 부당하지 않다.
# 2. 단 **기다릴 기간을 합의한 뒤 그 기간에 비례하여**(*a norma di quello*) 정해야 하고,
#    변덕·탐욕에 따라, 구매자의 절박함에 편승해 정해서는 안 된다.
#
# 즉 쟁점은 "가산이 있느냐"가 아니라 **"기간과 무관한 정액 가산이냐"** 이다.
# 이 노트북은 그 정액 가산 $1/3$ 을 기간별 실효 연이율로 환산해,
# 오를란디의 *"questo frutto non senta di usura"*(이 이자가 고리대 냄새가 나서는 안 된다)
# 라는 판단이 산수로 뒷받침되는지 확인한다.
#
# ## 모형
#
# 현금가를 $P$, 외상가를 $P_{\text{cr}}$, 상환까지의 기간을 $T$개월이라 하자.
#
# $$P_{\text{cr}} = P\left(1 + \tfrac{1}{3}\right) = \tfrac{4}{3}P$$
#
# 이 거래는 실질적으로 **원금 $P$ 를 $T$개월 빌려주고 이자 $P/3$ 를 받는 대출**이다
# (오를란디 자신의 표현: *rilasciar denaro a frutto*). 실효 연이율은 두 방식으로 잡을 수 있다.
#
# $$r_{\text{simple}} = \frac{1/3}{T/12}, \qquad
#   r_{\text{eff}} = \left(\frac{4}{3}\right)^{12/T} - 1$$
#
# 앞은 단리(연 환산), 뒤는 복리(같은 조건으로 계속 굴린다고 가정한 실효 연이율)다.

# %%
MARKUP = 1 / 3  # 오를란디가 지적한 가산율: 현금가의 3분의 1
LEGAL_RATE = 0.05  # 당대 관행적 '정당한 이자' 수준(연 5% 내외) — 비교 기준선


def _show(fig):
    try:
        from IPython import get_ipython

        if get_ipython() is not None:  # VSCode 셀/Jupyter에서만 렌더링
            fig.show()
    except ImportError:
        pass


def r_simple(markup: float, months: float) -> float:
    """단리 기준 연 환산 이율."""
    return markup / (months / 12)


def r_eff(markup: float, months: float) -> float:
    """복리 기준 실효 연이율."""
    return (1 + markup) ** (12 / months) - 1


print(f"가산율        = {MARKUP:.4f}  (= 1/3)")
print(f"외상가/현금가 = {1 + MARKUP:.4f}  (= 4/3)")
print(f"비교 기준선   = 연 {LEGAL_RATE:.1%}")
# 출력:
# 가산율        = 0.3333  (= 1/3)
# 외상가/현금가 = 1.3333  (= 4/3)
# 비교 기준선   = 연 5.0%

# %% [markdown]
# ## 1단계 — 기간별 실효 연이율 표
#
# 같은 "3분의 1"이 기간에 따라 완전히 다른 이율이 된다.
# 오를란디가 "기간에 비례해서 정하라"고 요구한 이유가 여기서 바로 드러난다.

# %%
TERMS = [1, 3, 6, 12, 24]  # 상환 기간(개월)

print(f"{'기간(개월)':>10} | {'단리 연이율':>12} | {'복리 실효연이율':>16} | {'5% 대비 배수(단리)':>18}")
print("-" * 68)
for t in TERMS:
    rs, re_ = r_simple(MARKUP, t), r_eff(MARKUP, t)
    print(f"{t:>10} | {rs:>11.1%} | {re_:>15.1%} | {rs / LEGAL_RATE:>17.1f}x")
# 출력:
#  기간(개월) |  단리 연이율 |  복리 실효연이율 |  5% 대비 배수(단리)
# --------------------------------------------------------------------
#          1 |      400.0% |         3056.9% |              80.0x
#          3 |      133.3% |          216.0% |              26.7x
#          6 |       66.7% |           77.8% |              13.3x
#         12 |       33.3% |           33.3% |               6.7x
#         24 |       16.7% |           15.5% |               3.3x

# %% [markdown]
# 읽는 법:
#
# - **3개월** 외상이면 단리로 연 133%, 복리로 연 216%. 스콜라 기준으로는 논란의 여지가 없는 고리대다.
# - **12개월**을 온전히 기다려 주어도 연 33.3% — 관행적 '정당한 이자'의 약 **6.7배**.
# - 기간이 짧을수록 폭발한다. 정액 가산은 $r \propto 1/T$ 이므로 $T \to 0$ 에서 발산한다.
#
# 즉 상인이 "3분의 1"이라는 **하나의 숫자**를 쓰는 순간, 그 숫자는 기간이 짧은 거래에서
# 자동으로 극단적 고리대가 된다. 오를란디의 요구는 사실상
# **"$1/3$ 을 고정하지 말고 $r \cdot T/12$ 로 계산하라"** 는 것이다.

# %% [markdown]
# ## 2단계 — 역산: 3분의 1이 '정당해지는' 기간은?
#
# 반대 방향으로 물어보자. 가산 $1/3$ 이 연 5%에 해당하려면 상환 기간이 얼마여야 하는가?
#
# $$\left(\frac{4}{3}\right)^{12/T} - 1 = r \;\Longrightarrow\;
#   T = \frac{12\,\ln(4/3)}{\ln(1+r)}
#   \qquad\text{(단리: } T = \frac{12 \cdot (1/3)}{r}\text{)}$$

# %%
import math


def break_even_months_eff(markup: float, rate: float) -> float:
    return 12 * math.log(1 + markup) / math.log(1 + rate)


def break_even_months_simple(markup: float, rate: float) -> float:
    return 12 * markup / rate


print(f"{'목표 연이율':>10} | {'필요 기간(단리)':>16} | {'필요 기간(복리)':>16}")
print("-" * 50)
for rate in [0.05, 0.06, 0.10, 0.3333]:
    bs = break_even_months_simple(MARKUP, rate)
    be = break_even_months_eff(MARKUP, rate)
    print(f"{rate:>10.2%} | {bs:>11.1f} 개월 | {be:>11.1f} 개월")
# 출력:
# 목표 연이율 |   필요 기간(단리) |   필요 기간(복리)
# --------------------------------------------------
#      5.00% |        80.0 개월 |        70.8 개월
#      6.00% |        66.7 개월 |        59.2 개월
#     10.00% |        40.0 개월 |        36.2 개월
#     33.33% |        12.0 개월 |        12.0 개월

# %%
be = break_even_months_eff(MARKUP, LEGAL_RATE)
print(f"연 {LEGAL_RATE:.0%} 로 3분의 1 가산이 정당화되려면 약 {be:.1f}개월 = {be / 12:.1f}년을 기다려야 한다.")
# 출력: 연 5% 로 3분의 1 가산이 정당화되려면 약 70.8개월 = 5.9년을 기다려야 한다.

# %% [markdown]
# 상거래 외상이 **6년**짜리인 경우는 없다. 실제 외상 기간은 몇 달 단위이므로,
# "3분의 1"은 *lucrum cessans* 로 설명할 수 있는 범위를 한참 넘는다.
# 오를란디가 "탐욕(ingordigia)의 결과이며 부정한(innonesto) 이익"이라고 규정한 것은
# 도덕적 과장이 아니라 이 산수의 서술이다.

# %% [markdown]
# ## 3단계 — 시각화: $T$에 대한 실효 이율 곡선
#
# 로그 y축을 쓰면 짧은 기간에서의 폭발이 잘 보인다.
# 수평선 두 개는 비교 기준(연 5%)과, 참고로 12개월 시 이율(33.3%)이다.

# %%
import plotly.graph_objects as go

X_MAX = 84  # 5% 손익분기(≈71개월)까지 보이도록 x축을 7년까지 잡는다
months = [0.5 + 0.05 * i for i in range(int((X_MAX - 0.5) / 0.05) + 1)]
simple = [r_simple(MARKUP, t) * 100 for t in months]
compound = [r_eff(MARKUP, t) * 100 for t in months]

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=months,
        y=compound,
        mode="lines",
        name="복리 실효 연이율  (4/3)^(12/T) − 1",
        line=dict(color="#c0392b", width=3),
        hovertemplate="T=%{x:.1f}개월<br>연 %{y:.1f}%<extra></extra>",
    )
)
fig.add_trace(
    go.Scatter(
        x=months,
        y=simple,
        mode="lines",
        name="단리 연 환산  (1/3)/(T/12)",
        line=dict(color="#2471a3", width=3, dash="dash"),
        hovertemplate="T=%{x:.1f}개월<br>연 %{y:.1f}%<extra></extra>",
    )
)

# 기준선: 당대 관행적 '정당한 이자' 수준
fig.add_hline(y=LEGAL_RATE * 100, line=dict(color="#1e8449", width=2, dash="dot"))
fig.add_annotation(
    x=X_MAX * 0.33,
    y=math.log10(LEGAL_RATE * 100),
    text="연 5% — 당대 관행적 '정당한 이자' / Monte di Pieta 수준",
    showarrow=False,
    yshift=12,
    font=dict(color="#1e8449", size=12),
)
fig.add_hline(y=MARKUP * 100, line=dict(color="#7f8c8d", width=1, dash="dot"))
fig.add_annotation(
    x=X_MAX * 0.62,
    y=math.log10(MARKUP * 100),
    text="연 33.3% (T=12개월)",
    showarrow=False,
    yshift=12,
    font=dict(color="#7f8c8d", size=12),
)

# 표에 쓴 대표 기간 표시
fig.add_trace(
    go.Scatter(
        x=TERMS,
        y=[r_eff(MARKUP, t) * 100 for t in TERMS],
        mode="markers+text",
        name="대표 기간 (1·3·6·12·24개월)",
        marker=dict(color="#c0392b", size=10, symbol="circle", line=dict(color="white", width=1.5)),
        text=[f"{r_eff(MARKUP, t) * 100:,.0f}%" for t in TERMS],
        textposition="top right",
        textfont=dict(size=10),
        hoverinfo="skip",
    )
)

# 3분의 1이 연 5%가 되는 지점
fig.add_trace(
    go.Scatter(
        x=[be],
        y=[LEGAL_RATE * 100],
        mode="markers+text",
        name=f"5%가 되는 기간 ≈ {be:.0f}개월",
        marker=dict(color="#1e8449", size=11, symbol="diamond"),
        text=[f"{be:.0f}개월 ≈ {be / 12:.1f}년"],
        textposition="bottom center",
        textfont=dict(size=11, color="#1e8449"),
        hoverinfo="skip",
    )
)

fig.update_layout(
    title=dict(
        text="'현금가 대비 3분의 1 가산'의 실효 연이율<br>"
        "<sub>오를란디, Iconologia MERCATURA — 짧은 외상일수록 고리대에 가까워진다</sub>",
        x=0.5,
    ),
    xaxis=dict(title="상환 기간 T (개월)", range=[0, X_MAX], dtick=6),
    yaxis=dict(title="실효 연이율 (%, 로그 축)", type="log", range=[math.log10(1), math.log10(5000)]),
    template="plotly_white",
    legend=dict(x=0.98, y=0.98, xanchor="right", yanchor="top", bgcolor="rgba(255,255,255,0.85)"),
    width=980,
    height=620,
    margin=dict(t=100, r=40),
)

_show(fig)
fig.write_image("expy.png", scale=2)
print("expy.png 저장 완료")
# 출력: expy.png 저장 완료

# %% [markdown]
# ## 4단계 (보너스) — 스콜라 예외 법리로 역산하기
#
# 스콜라 전통은 원금 위험(*periculum sortis*)에 대한 보상은 허용했다.
# 그렇다면 **부도 위험만으로** 3분의 1 가산을 정당화하려면 부도 확률이 얼마여야 하는가?
#
# 부도 확률 $p$, 부도 시 회수율 $\rho$ 라 하면 외상 판매의 기대 회수액은
#
# $$\mathbb{E}[\text{회수}] = (1-p)\cdot\tfrac{4}{3}P + p\cdot\rho\cdot\tfrac{4}{3}P$$
#
# 이것이 현금가 $P$ 와 같아지는 지점(= 가산이 순전히 위험 보상일 뿐 초과 이익이 0인 지점)은
#
# $$\tfrac{4}{3}\bigl(1-p(1-\rho)\bigr) = 1 \;\Longrightarrow\; p = \frac{1}{4(1-\rho)}$$
#
# 회수율 $\rho = 0$ (전손)이면 $p = 1/4$, 즉 **부도 확률 25%** 다.

# %%
def break_even_default_prob(markup: float, recovery: float) -> float:
    """기대 회수 = 현금가가 되는 부도 확률. 1을 넘으면 '어떤 p로도 정당화 불가'."""
    loss = (1 + markup) * (1 - recovery)
    if loss <= 0:
        return float("inf")
    return markup / loss


print(f"{'회수율 rho':>10} | {'필요 부도확률 p':>16}")
print("-" * 32)
for rho in [0.0, 0.25, 0.5, 0.75]:
    p = break_even_default_prob(MARKUP, rho)
    flag = "" if p <= 1 else "  <- 불가능(p>1)"
    print(f"{rho:>10.0%} | {p:>15.1%}{flag}")
# 출력:
# 회수율 rho |   필요 부도확률 p
# --------------------------------
#         0% |           25.0%
#        25% |           33.3%
#        50% |           50.0%
#        75% |          100.0%

# %% [markdown]
# **해석.** 전손 가정에서도 부도 확률이 **25%** 는 되어야 3분의 1 가산이 순수한 위험 프리미엄이 된다.
# 오를란디 자신이 상인에게 요구한 것은 "계약 상대의 신용을 **미리 확인해 안전을 확보하라**
# (*porsi prima in sicuro intorno la Persona*)"였다. 그렇게 선별한 상대에게 25%의 부도 확률을
# 전제하는 것은 자기모순이다. 결국 3분의 1 가산은 *periculum sortis* 로도 설명되지 않는다.

# %%
# 종합: 세 가지 정당화 명목을 동시에 얹어도 3분의 1은 남는다.
#   - lucrum cessans : 연 5%, T=6개월 → 2.5%
#   - damnum emergens: 사무·회수 비용을 넉넉히 3%로 가정
#   - periculum sortis: 선별된 상대의 부도 확률 3%, 전손 → 약 3%
T = 6
justified = LEGAL_RATE * (T / 12) + 0.03 + 0.03
print(f"T={T}개월 기준 정당화 가능한 가산 합계 ≈ {justified:.1%}")
print(f"오를란디가 지적한 실제 가산      = {MARKUP:.1%}")
print(f"설명되지 않는 초과분             ≈ {MARKUP - justified:.1%}  <- '부정한 이익(guadagno innonesto)'")
# 출력:
# T=6개월 기준 정당화 가능한 가산 합계 ≈ 8.5%
# 오를란디가 지적한 실제 가산      = 33.3%
# 설명되지 않는 초과분             ≈ 24.8%  <- '부정한 이익(guadagno innonesto)'

# %% [markdown]
# ## 정리
#
# | 물음 | 답 |
# |---|---|
# | 3개월 외상에서 1/3 가산 = 연이율? | 단리 133%, 복리 216% |
# | 12개월이라도? | 33.3% — 관행 이자(5%)의 6.7배 |
# | 1/3이 연 5%가 되려면? | 약 71개월(≈5.9년) 기다려야 함 |
# | 위험만으로 정당화하려면? | 부도 확률 25%(전손 가정) |
# | 6개월 기준 설명 안 되는 초과분 | 약 25%p |
#
# 오를란디의 두 문장이 이 수치로 정확히 번역된다.
#
# - *"altro non fa, che rilasciar denaro a frutto"* — 그것은 매매가 아니라 **이자부 대출**이다.
#   그러므로 **연이율로 환산해 볼 수 있다**(= 위 계산이 성립하는 근거).
# - *"questo frutto non senta di usura"* — 그런데 환산해 보면 그 이자는
#   당대 어떤 정당화 명목으로도 설명되지 않는 수준이다. 그래서 **고리대에 가깝다**.
#
# 그리고 그가 제시한 처방 — **"기간을 합의하고 그 기간에 비례하여 정하라"** — 는
# 정액 가산 $1/3$ 을 $r \cdot T/12$ 로 바꾸라는 말, 즉 **정액을 이율로 바꾸라**는 말이다.
# 이것이 근대적 이자 개념이 스콜라 윤리 안에서 자라난 경로 그 자체다.
