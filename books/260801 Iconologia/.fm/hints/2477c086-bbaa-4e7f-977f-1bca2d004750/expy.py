# %% [markdown]
# # 컴퍼스와 자: 기하학적 비례 vs 산술적 비례
#
# Ripa/Mariottelli의 `Prattica`(실천)는 두 개의 도구를 든다.
#
# | 도구 | 실천의 종류 | 정의 | 비례 |
# |---|---|---|---|
# | **컴퍼스** (정해진 치수 없음, 사물에 맞춤) | 자유(liberale) | 분배 정의 | **기하학적** |
# | **자** (공적 합의로 확정된 치수) | 기계(mecanica) | 교환 정의 | **산술적** |
#
# 이 노트북은 두 비례를 **실제 수치로 계산·대조**한다.
#
# - 분배 정의(기하학적): 공로 $A_i$ 에 **비례**해 나눈다. 보존되는 것은 **비(ratio)**.
#   $$\frac{A_1}{A_2} = \frac{s_1}{s_2} \qquad\Longleftrightarrow\qquad s_i = S \cdot \frac{A_i}{\sum_j A_j}$$
# - 교환 정의(산술적): 사람의 가치를 묻지 않고 **손해와 이득의 차**를 0으로 만든다.
#   $$x^{*} = \frac{x_1 + x_2}{2}, \qquad \text{이전액} = \frac{\text{초과분}}{2}$$

# 필요 패키지: plotly, kaleido  (pip install plotly kaleido)

# %%
from fractions import Fraction


def _show(fig):
    try:
        from IPython import get_ipython

        if get_ipython() is not None:  # VSCode 셀/Jupyter에서만 렌더링
            fig.show()
    except ImportError:
        pass


# %% [markdown]
# ## 1. 컴퍼스 — 분배 정의 (기하학적 비례)
#
# 도시가 공적 재화 **1200 두카토**를 세 시민에게 나눈다.
# 각자의 `axia`(가치·공로)는 공동체가 인정한 값이다. 컴퍼스에는 정해진 눈금이 없으므로
# "얼마가 공로인가"는 **관습(costume)** 이 정한다 — 여기서는 6 : 3 : 1 로 주어졌다고 하자.

# %%
TOTAL = 1200
merit = {"Aulo": 6, "Bruto": 3, "Caio": 1}

merit_sum = sum(merit.values())
share = {k: Fraction(TOTAL * v, merit_sum) for k, v in merit.items()}

for k in merit:
    print(f"{k:6s} 공로={merit[k]:2d}  몫={float(share[k]):8.2f}")
print("합계:", float(sum(share.values())))
# 출력:
# Aulo   공로= 6  몫=  720.00
# Bruto  공로= 3  몫=  360.00
# Caio   공로= 1  몫=  120.00
# 합계: 1200.0

# %% [markdown]
# ### 비례가 실제로 보존되는지 확인
#
# 기하학적 비례의 정의는 $A_i / A_j = s_i / s_j$ 다. **비**가 같아야 하고, **차**는 같지 않아도 된다.

# %%
pairs = [("Aulo", "Bruto"), ("Bruto", "Caio"), ("Aulo", "Caio")]
for a, b in pairs:
    r_merit = Fraction(merit[a], merit[b])
    r_share = share[a] / share[b]
    print(
        f"{a:5s}:{b:5s}  공로비={r_merit}  몫비={r_share}  "
        f"비 동일={r_merit == r_share}  |  몫의 차={float(share[a] - share[b]):7.2f}"
    )
# 출력:
# Aulo :Bruto  공로비=2  몫비=2  비 동일=True  |  몫의 차= 360.00
# Bruto:Caio   공로비=3  몫비=3  비 동일=True  |  몫의 차= 240.00
# Aulo :Caio   공로비=6  몫비=6  비 동일=True  |  몫의 차= 600.00

# %% [markdown]
# **관찰**: 비는 전부 정확히 일치하지만 차는 360 / 240 / 600 으로 전부 다르다.
# 컴퍼스는 다리를 벌려 **비율**을 옮기는 도구이므로 이 정의에 맞다.
#
# ### 만약 자(산술적 균등)로 분배했다면?
# 공로를 무시하고 1200을 3등분하면 각자 400. 공로가 6인 사람도 1인 사람도 같은 몫을 받는다.
# 아리스토텔레스에게 이것은 정의가 아니라 **비례의 위반**이다.

# %%
equal = Fraction(TOTAL, 3)
for k in merit:
    print(f"{k:6s} 기하학적={float(share[k]):8.2f}  산술적(오용)={float(equal):8.2f}  차={float(share[k] - equal):+8.2f}")
# 출력:
# Aulo   기하학적=  720.00  산술적(오용)=  400.00  차= +320.00
# Bruto  기하학적=  360.00  산술적(오용)=  400.00  차=  -40.00
# Caio   기하학적=  120.00  산술적(오용)=  400.00  차= -280.00

# %% [markdown]
# ### 정치체제가 바뀌면 `axia`의 내용이 바뀐다 (NE V.3, 1131a)
# 민주정은 자유민 신분, 귀족정은 덕, 금권정은 재산을 `axia`로 삼는다.
# 컴퍼스의 벌어진 폭이 공동체마다 다르다는 뜻이다.

# %%
regimes = {
    "민주정 (신분: 모두 자유민)": {"Aulo": 1, "Bruto": 1, "Caio": 1},
    "귀족정 (덕)": {"Aulo": 2, "Bruto": 5, "Caio": 3},
    "금권정 (재산)": {"Aulo": 6, "Bruto": 3, "Caio": 1},
}
dist_by_regime = {}
for name, ax in regimes.items():
    tot = sum(ax.values())
    row = {k: TOTAL * v / tot for k, v in ax.items()}
    dist_by_regime[name] = row
    print(f"{name:26s} " + "  ".join(f"{k}={row[k]:7.2f}" for k in merit))
# 출력:
# 민주정 (신분: 모두 자유민)           Aulo= 400.00  Bruto= 400.00  Caio= 400.00
# 귀족정 (덕)                    Aulo= 240.00  Bruto= 600.00  Caio= 360.00
# 금권정 (재산)                   Aulo= 720.00  Bruto= 360.00  Caio= 120.00

# %% [markdown]
# ## 2. 자 — 교환 정의 (산술적 비례)
#
# 아울루스가 브루투스에게서 **90 두카토**만큼을 부당하게 취했다. 거래 전 둘의 재산은 각각 500, 300.
# 재판관은 두 사람이 **누구인지 묻지 않는다** (NE V.4, 1132a: "훌륭한 사람이 나쁜 사람의 것을 빼앗았는지는
# 아무 차이가 없다. 법은 손해의 크기만 본다").
#
# $$\text{초과분} = x_1 - x_2, \qquad \text{이전액} = \frac{\text{초과분}}{2}$$

# %%
before = {"Aulo": 500, "Bruto": 300}
harm = 90  # 아울루스의 이득 = 브루투스의 손해

after = {"Aulo": before["Aulo"] + harm, "Bruto": before["Bruto"] - harm}
print("침해 후:", after)

# 아리스토텔레스의 선분 비유: 이득과 손해라는 '두 선분'을 균등화한다
gain, loss = harm, -harm
excess = gain - loss  # 180
transfer = excess / 2  # 90
mean = (gain + loss) / 2  # 0

print(f"이득={gain:+d}  손해={loss:+d}  초과분={excess}  중간={mean}  이전액={transfer}")
print("시정 후:", {"Aulo": after["Aulo"] - transfer, "Bruto": after["Bruto"] + transfer})
# 출력:
# 침해 후: {'Aulo': 590, 'Bruto': 210}
# 이득=+90  손해=-90  초과분=180  중간=0.0  이전액=90.0
# 시정 후: {'Aulo': 500.0, 'Bruto': 300.0}

# %% [markdown]
# **관찰**: 시정 정의는 재산을 **같게** 만들지 않는다 (500 ≠ 300). 원상태로 되돌릴 뿐이다.
# 균등화되는 것은 재산이 아니라 **이득과 손해의 차**다: $+90$ 과 $-90$ 을 각각 $0$ 으로.
#
# ### 기하학적으로 시정하면? (교환 정의에 공로를 끌어들이는 오용)
# 공로 6 : 3 을 근거로 아울루스에게 초과분을 유리하게 배분하면 브루투스는 손해를 다 회복하지 못한다.

# %%
ratio_transfer = excess * Fraction(merit["Bruto"], merit["Aulo"] + merit["Bruto"])  # 180 * 3/9 = 60
print(f"기하학적(오용) 이전액={float(ratio_transfer):.2f}  →  Bruto 최종={after['Bruto'] + float(ratio_transfer):.2f}")
print(f"산술적(정답) 이전액={transfer:.2f}  →  Bruto 최종={after['Bruto'] + transfer:.2f}")
print(f"미회복 손해={float(transfer - ratio_transfer):.2f}")
# 출력:
# 기하학적(오용) 이전액=60.00  →  Bruto 최종=270.00
# 산술적(정답) 이전액=90.00  →  Bruto 최종=300.00
# 미회복 손해=30.00

# %% [markdown]
# ## 3. 척도의 성격: 컴퍼스는 눈금이 없고, 자는 눈금이 있다
#
# 두 정의를 **하나의 함수 파라미터**로 통합해 보면 차이가 선명해진다.
# 공로가 $A_1 : A_2$ 인 두 사람에게 $S$ 를 나눌 때
#
# $$s_1(\lambda) = S\left[\frac{1}{2} + \lambda\left(\frac{A_1}{A_1+A_2} - \frac{1}{2}\right)\right]$$
#
# - $\lambda = 0$ : 순수 산술적 균등 (자) — 공로를 전혀 반영하지 않음
# - $\lambda = 1$ : 순수 기하학적 비례 (컴퍼스) — 공로에 완전 비례
#
# 컴퍼스의 "정해진 비례 없음(non ha proporzioni terminate)"이란 곧 이 $\lambda$ 와 $A_i$ 를
# **관습이 정한다**는 뜻이다. 반면 자의 눈금은 공적 합의로 못 박혀 움직이지 않는다.


# %%
def blend(lam, total=TOTAL, a1=6, a2=3):
    p = a1 / (a1 + a2)
    s1 = total * (0.5 + lam * (p - 0.5))
    return s1, total - s1


for lam in (0.0, 0.25, 0.5, 0.75, 1.0):
    s1, s2 = blend(lam)
    print(f"lambda={lam:4.2f}  s1={s1:7.2f}  s2={s2:7.2f}  s1/s2={s1 / s2:5.3f}  s1-s2={s1 - s2:+8.2f}")
# 출력:
# lambda=0.00  s1= 600.00  s2= 600.00  s1/s2=1.000  s1-s2=   +0.00
# lambda=0.25  s1= 650.00  s2= 550.00  s1/s2=1.182  s1-s2= +100.00
# lambda=0.50  s1= 700.00  s2= 500.00  s1/s2=1.400  s1-s2= +200.00
# lambda=0.75  s1= 750.00  s2= 450.00  s1/s2=1.667  s1-s2= +300.00
# lambda=1.00  s1= 800.00  s2= 400.00  s1/s2=2.000  s1-s2= +400.00

# %% [markdown]
# ## 4. 시각화
#
# - 왼쪽: 컴퍼스(기하학적) — 공로에 비례한 분배. **비**가 보존됨
# - 가운데: 자(산술적) — 침해와 시정. **차**가 0으로 균등화됨
# - 오른쪽: $\lambda$ 를 0→1 로 움직일 때 몫의 **비**와 **차**가 어떻게 변하는가

# %%
import plotly.graph_objects as go
from plotly.subplots import make_subplots

C_COMPASS = "#8c6d3f"  # 컴퍼스 = 흙/황갈색(tanè) 계열
C_RULE = "#3f6d8c"  # 자 = 청색 계열
C_MISUSE = "#b04a3a"

fig = make_subplots(
    rows=1,
    cols=3,
    subplot_titles=(
        "컴퍼스: 분배 정의 (기하학적)",
        "자: 교환 정의 (산술적)",
        "척도의 연속체 (λ)",
    ),
    specs=[[{}, {}, {"secondary_y": True}]],
    horizontal_spacing=0.09,
)

# --- (1) 분배 정의: 기하학적 vs 균등분배
names = list(merit.keys())
fig.add_bar(
    x=names,
    y=[float(share[k]) for k in names],
    name="기하학적 비례 (공로 6:3:1)",
    marker_color=C_COMPASS,
    text=[f"{float(share[k]):.0f}" for k in names],
    textposition="outside",
    row=1,
    col=1,
)
fig.add_bar(
    x=names,
    y=[float(equal)] * 3,
    name="산술적 균등 (오용)",
    marker_color=C_MISUSE,
    opacity=0.55,
    text=[f"{float(equal):.0f}"] * 3,
    textposition="outside",
    row=1,
    col=1,
)

# --- (2) 교환 정의: 이득/손해의 산술적 균등화
stages = ["거래 전", "침해 후", "시정 후"]
aulo = [before["Aulo"], after["Aulo"], after["Aulo"] - transfer]
bruto = [before["Bruto"], after["Bruto"], after["Bruto"] + transfer]
fig.add_bar(x=stages, y=aulo, name="Aulo 재산", marker_color=C_RULE, text=aulo, textposition="outside", row=1, col=2)
fig.add_bar(
    x=stages,
    y=bruto,
    name="Bruto 재산",
    marker_color=C_RULE,
    opacity=0.5,
    text=bruto,
    textposition="outside",
    row=1,
    col=2,
)
fig.add_annotation(
    x="침해 후",
    y=after["Aulo"] + 70,
    text=f"초과분 {excess} → 절반 {transfer:.0f} 이전",
    showarrow=False,
    font=dict(size=10, color=C_MISUSE),
    row=1,
    col=2,
)

# --- (3) lambda 연속체: 비(ratio) vs 차(difference)
lams = [i / 100 for i in range(101)]
ratios, diffs = [], []
for lam in lams:
    s1, s2 = blend(lam)
    ratios.append(s1 / s2)
    diffs.append(s1 - s2)

fig.add_scatter(
    x=lams, y=ratios, name="몫의 비 s₁/s₂", line=dict(color=C_COMPASS, width=3), row=1, col=3, secondary_y=False
)
fig.add_scatter(
    x=lams,
    y=diffs,
    name="몫의 차 s₁−s₂",
    line=dict(color=C_RULE, width=3, dash="dash"),
    row=1,
    col=3,
    secondary_y=True,
)
for lam, label, col in ((0.0, "자<br>(산술)", C_RULE), (1.0, "컴퍼스<br>(기하)", C_COMPASS)):
    fig.add_vline(x=lam, line=dict(color=col, width=1, dash="dot"), row=1, col=3)
    fig.add_annotation(
        x=lam, y=1.06, xref="x3", yref="paper", text=label, showarrow=False, font=dict(size=10, color=col)
    )

fig.update_yaxes(title_text="몫 (두카토)", range=[0, 880], row=1, col=1)
fig.update_yaxes(title_text="재산 (두카토)", range=[0, 720], row=1, col=2)
fig.update_xaxes(title_text="λ  (0 = 자, 1 = 컴퍼스)", row=1, col=3)
fig.update_yaxes(title_text="비 s₁/s₂", color=C_COMPASS, row=1, col=3, secondary_y=False)
fig.update_yaxes(title_text="차 s₁−s₂", color=C_RULE, row=1, col=3, secondary_y=True)
fig.update_layout(
    title="Prattica의 두 도구 — 기하학적 비례(분배 정의) vs 산술적 비례(교환 정의)",
    template="plotly_white",
    height=520,
    width=1500,
    barmode="group",
    legend=dict(orientation="h", y=-0.22, x=0.5, xanchor="center"),
    margin=dict(t=90, b=110),
)

_show(fig)
fig.write_image("expy.png", scale=2)
print("saved expy.png")
# 출력: saved expy.png
