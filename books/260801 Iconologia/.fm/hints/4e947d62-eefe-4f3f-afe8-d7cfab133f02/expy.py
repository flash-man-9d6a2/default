# %% [markdown]
# # Magnum vectigal Parsimonia — "검약은 큰 세입이다"
#
# 리파 『이코놀로지아』의 **PARSIMONIA** 항목은 두 개의 정량적 주장을 담고 있다.
#
# 1. **아이스키네스**(소크라테스학파): 식비 지출을 줄임으로써 *자기 자신에게서 이자를 받는다*
#    (`da se stesso pigliava ad usura con lo sminuire la spesa`).
# 2. **아리스토텔레스**: `Opulentiores enim fiunt non ii modo, qui ad opes aliquid addant,`
#    `sed ii quoque qui de sumptibus detrahunt.`
#    — 부유해지는 것은 재산에 더하는 자만이 아니라 **지출에서 덜어내는 자** 또한 그렇다.
#
# 이 스크립트는 두 주장이 단순한 수사가 아니라 **회계적 항등식**임을 확인한다.

# %%
# 필요 패키지: plotly, kaleido  (pip install plotly kaleido)
from __future__ import annotations

import os

import plotly.graph_objects as go
from plotly.subplots import make_subplots


def _show(fig):
    try:
        from IPython import get_ipython

        if get_ipython() is not None:  # VSCode 셀/Jupyter에서만 렌더링
            fig.show()
    except ImportError:
        pass


HERE = os.path.dirname(os.path.abspath(__file__))

# %% [markdown]
# ## 1단계 — 가계의 기본 항등식
#
# 수입 $I$, 지출 $E$ 일 때 순저축(= 그 해에 늘어난 재산)은
#
# $$ S = I - E $$
#
# 따라서 $\partial S/\partial I = +1$ 이고 $\partial S/\partial E = -1$ 이다.
# **수입 1원 증대와 지출 1원 절감은 순저축에 대해 정확히 같은 크기의 효과를 갖는다.**
# 이것이 아리스토텔레스가 말한 "더하는 자"와 "덜어내는 자"의 등가성이다.


# %%
def net_saving(income: float, expense: float) -> float:
    return income - expense


I0, E0 = 3_000_000.0, 2_700_000.0  # 월 수입 300만, 월 지출 270만
delta = 200_000.0  # 개선 폭 20만

base = net_saving(I0, E0)
add_income = net_saving(I0 + delta, E0)  # 수입을 늘리는 자
cut_expense = net_saving(I0, E0 - delta)  # 지출을 덜어내는 자

print(f"기준 순저축        : {base:>12,.0f}")
print(f"수입 +{delta:,.0f} 시   : {add_income:>12,.0f}")
print(f"지출 -{delta:,.0f} 시   : {cut_expense:>12,.0f}")
print(f"두 전략이 동일한가?: {add_income == cut_expense}")
# 출력: 기준 순저축        :      300,000
# 출력: 수입 +200,000 시   :      500,000
# 출력: 지출 -200,000 시   :      500,000
# 출력: 두 전략이 동일한가?: True

# %% [markdown]
# ### 세후로 보면 절감이 오히려 우월하다
#
# 실제로는 추가 수입에 세율 $\tau$ 가 붙지만, 절감된 지출은 과세되지 않는다.
# 세후 순저축 증가분은
#
# $$ \Delta S_{\text{수입}} = (1-\tau)\,\Delta, \qquad \Delta S_{\text{절감}} = \Delta $$
#
# 즉 지출 1원을 줄이는 것은 **세전 수입 $\Delta/(1-\tau)$ 원을 더 버는 것**과 맞먹는다.
# 리파의 `ottima risoluzione è per accrescere l'entrata, il riformar le spese`
# ("수입을 늘리는 최선의 방책은 지출을 개혁하는 것")가 문자 그대로 성립한다.

# %%
TAU = 0.24  # 한계세율 24% 가정
after_tax_income = (1 - TAU) * delta
equivalent_gross = delta / (1 - TAU)

print(f"세율 {TAU:.0%} 하에서")
print(f"  추가수입 {delta:,.0f} → 세후 {after_tax_income:,.0f}")
print(f"  지출절감 {delta:,.0f} → 세후 {delta:,.0f}  (과세 없음)")
print(f"  절감 {delta:,.0f}과 등가인 세전 수입 = {equivalent_gross:,.0f}")
# 출력: 세율 24% 하에서
# 출력:   추가수입 200,000 → 세후 152,000
# 출력:   지출절감 200,000 → 세후 200,000  (과세 없음)
# 출력:   절감 200,000과 등가인 세전 수입 = 263,158

# %% [markdown]
# ## 2단계 — 아이스키네스의 "자기에게서 받는 이자"
#
# 아이스키네스는 절감을 **대금업(usura)** 으로 비유했다. 이 비유는 정확하다.
# 원금 $P$ 를 이율 $r$ 로 빌려주면 매년 $rP$ 의 이자가 나온다.
# 매년 $s$ 원을 절감하는 것은 매년 $s$ 원의 영구 현금흐름(perpetuity)이므로,
# 그것을 만들어 내는 데 필요한 가상의 원금은
#
# $$ P = \frac{s}{r} $$
#
# 다시 말해 **연 절감액 $s$ 는 자본 $s/r$ 를 소유한 것과 등가**다.
# 이것이 `Magnum vectigal Parsimonia` — 검약이 하나의 **세입원(vectigal)** 인 이유다.


# %%
def implied_capital(annual_saving: float, r: float) -> float:
    """연 절감액 s가 이율 r 하에서 상당하는 자본가치 s/r."""
    return annual_saving / r


s_year = delta * 12  # 연 절감액 = 240만
for r in (0.02, 0.03, 0.05, 0.08):
    print(f"r={r:>5.0%} → 상당 자본 {implied_capital(s_year, r):>14,.0f}  ({s_year / r / s_year:.1f}배)")
# 출력: r=   2% → 상당 자본    120,000,000  (50.0배)
# 출력: r=   3% → 상당 자본     80,000,000  (33.3배)
# 출력: r=   5% → 상당 자본     48,000,000  (20.0배)
# 출력: r=   8% → 상당 자본     30,000,000  (12.5배)

# %% [markdown]
# 검증: 자본 $P=s/r$ 을 실제로 굴리면 이자가 정확히 $s$ 가 되는지 확인한다.
# 두 값이 일치하면 "절감 = 이자 수취"라는 아이스키네스의 등식이 성립한다.

# %%
r_test = 0.05
P = implied_capital(s_year, r_test)
interest = P * r_test
print(f"가상 원금 {P:,.0f} × {r_test:.0%} = {interest:,.0f}")
print(f"연 절감액                    = {s_year:,.0f}")
print(f"일치? {abs(interest - s_year) < 1e-9}")
# 출력: 가상 원금 48,000,000 × 5% = 2,400,000
# 출력: 연 절감액                    = 2,400,000
# 출력: 일치? True

# %% [markdown]
# ## 3단계 — 절감액의 복리 누적
#
# 절감액을 다시 이율 $r$ 로 재투자하면 $n$ 년 후 잔고는 연금 미래가치가 된다.
#
# $$ FV(n) = s \cdot \frac{(1+r)^n - 1}{r} $$
#
# 원금 투입 없이 **지출을 깎기만 해서** 자산이 쌓인다는 점이 요지다.


# %%
def fv_annuity(s: float, r: float, n: int) -> float:
    if r == 0:
        return s * n
    return s * ((1 + r) ** n - 1) / r


for n in (1, 5, 10, 20, 30):
    fv = fv_annuity(s_year, 0.05, n)
    contributed = s_year * n
    print(f"{n:>2}년: 잔고 {fv:>14,.0f} | 절감 원금 {contributed:>12,.0f} | 이자분 {fv - contributed:>12,.0f}")
# 출력:  1년: 잔고      2,400,000 | 절감 원금    2,400,000 | 이자분            0
# 출력:  5년: 잔고     13,261,515 | 절감 원금   12,000,000 | 이자분    1,261,515
# 출력: 10년: 잔고     30,186,942 | 절감 원금   24,000,000 | 이자분    6,186,942
# 출력: 20년: 잔고     79,358,290 | 절감 원금   48,000,000 | 이자분   31,358,290
# 출력: 30년: 잔고    159,453,234 | 절감 원금   72,000,000 | 이자분   87,453,234

# %% [markdown]
# ## 4단계 — 컴퍼스: 반지름을 넘지 않는 절제
#
# 리파는 컴퍼스가 **"자기 원주 밖으로 한 점도 나가지 않는다"** 고 하며,
# 그처럼 검약은 *정직함과 합리성의 한도*를 넘지 않는다고 말한다.
# 즉 검약은 지출을 0으로 만드는 것(= 인색, avarizia)이 아니라,
# **필요(need)라는 하한과 수입(income)이라는 상한 사이에** 지출을 두는 것이다.
#
# $$ E_{\text{need}} \le E \le I $$
#
# 세네카가 덧붙이는 이유: `sine qua nullae opes sufficiunt`
# — 검약 없이는 **어떤 재산도 충분하지 않다.**


# %%
def within_compass(expense: float, need: float, income: float) -> str:
    if expense > income:
        return "낭비(prodigalità): 수입 초과 — Majorem censu define cultum"
    if expense < need:
        return "인색(avarizia): 필요 미달 — 컴퍼스 반지름 안쪽으로 붕괴"
    return "검약(parsimonia): 한도 내"


NEED = 1_800_000.0
for e in (3_400_000.0, 2_700_000.0, 2_500_000.0, 1_500_000.0):
    print(f"지출 {e:>10,.0f} → {within_compass(e, NEED, I0)}")
# 출력: 지출  3,400,000 → 낭비(prodigalità): 수입 초과 — Majorem censu define cultum
# 출력: 지출  2,700,000 → 검약(parsimonia): 한도 내
# 출력: 지출  2,500,000 → 검약(parsimonia): 한도 내
# 출력: 지출  1,500,000 → 인색(avarizia): 필요 미달 — 컴퍼스 반지름 안쪽으로 붕괴

# %% [markdown]
# ## 시각화
#
# - **왼쪽**: 연 절감액이 이율 $r$ 하에서 상당하는 자본가치 $s/r$ — 낮은 이율일수록
#   같은 절감액이 더 큰 "세입원"으로 환산된다.
# - **오른쪽**: 절감액의 복리 누적($r=5\%$). 원금 투입은 0인데 잔고는 쌓인다.

# %%
rs = [0.01 + 0.001 * i for i in range(0, 91)]  # 1% ~ 10%
caps = [implied_capital(s_year, r) / 1e6 for r in rs]

years = list(range(0, 31))
fv_curve = [fv_annuity(s_year, 0.05, n) / 1e6 for n in years]
contrib_curve = [s_year * n / 1e6 for n in years]

fig = make_subplots(
    rows=1,
    cols=2,
    subplot_titles=(
        "연 절감액 240만의 상당 자본가치 s/r",
        "절감액의 복리 누적 (r=5%)",
    ),
)

fig.add_trace(
    go.Scatter(x=[r * 100 for r in rs], y=caps, mode="lines", name="s/r (백만원)", line=dict(width=3)),
    row=1,
    col=1,
)
for r_mark in (0.02, 0.05, 0.08):
    fig.add_trace(
        go.Scatter(
            x=[r_mark * 100],
            y=[implied_capital(s_year, r_mark) / 1e6],
            mode="markers+text",
            text=[f"{implied_capital(s_year, r_mark) / 1e6:.0f}M"],
            textposition="top right",
            showlegend=False,
            marker=dict(size=10),
        ),
        row=1,
        col=1,
    )

fig.add_trace(
    go.Scatter(x=years, y=fv_curve, mode="lines", name="잔고 FV(n)", line=dict(width=3)),
    row=1,
    col=2,
)
fig.add_trace(
    go.Scatter(x=years, y=contrib_curve, mode="lines", name="절감 원금 누계", line=dict(width=2, dash="dash")),
    row=1,
    col=2,
)

fig.update_xaxes(title_text="요구수익률 r (%)", row=1, col=1)
fig.update_yaxes(title_text="자본가치 (백만원)", row=1, col=1)
fig.update_xaxes(title_text="경과 연수", row=1, col=2)
fig.update_yaxes(title_text="금액 (백만원)", row=1, col=2)
fig.update_layout(
    title_text="Magnum vectigal Parsimonia — 절감액은 세입이자 자본이다",
    template="plotly_white",
    width=1100,
    height=480,
    legend=dict(orientation="h", y=-0.2),
)

_show(fig)
fig.write_image(os.path.join(HERE, "expy.png"), scale=2)
print("saved:", os.path.join(HERE, "expy.png"))
# 출력: saved: .../4e947d62-eefe-4f3f-afe8-d7cfab133f02/expy.png

# %% [markdown]
# ## 결론
#
# | 리파가 인용한 격언 | 대응하는 수식 |
# |---|---|
# | *Opulentiores fiunt … qui de sumptibus detrahunt* (아리스토텔레스) | $\partial S/\partial E = -1 = -\,\partial S/\partial I$ |
# | 아이스키네스: 지출 절감 = 자기에게서 받는 이자 | $s = rP \Leftrightarrow P = s/r$ |
# | *Magnum vectigal Parsimonia* | 절감액은 자본 $s/r$ 짜리 영구 세입원 |
# | 컴퍼스: 한도를 넘지 않음 | $E_{\text{need}} \le E \le I$ |
# | *Plus est servasse repertum quam quaesisse decus novum* (클라우디아누스) | 보전(확정적)이 획득(*casus inest illic*, 우연 개입)보다 우월 |
