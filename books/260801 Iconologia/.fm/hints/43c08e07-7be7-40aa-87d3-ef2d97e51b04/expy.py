# %% [markdown]
# # 정육면체는 왜 '고요(Quiete)'인가 — 다섯 정다면체의 안정성 수치 비교
#
# 체사레 리파 『이코놀로지아』의 **Quiete(고요/안식)** 항목:
#
# > "정육면체 받침대 위에 서서 오른손에 다림추를 받쳐 든 여인.
# > 정육면체는 플라톤이 (피타고라스의 제자 티마이오스 로크렌시스를 따라) 전하는 바
# > **대지(terra)** 를 뜻한다. 대지는 우주의 중심이라는 자기 고유의 자리에 있어
# > 움직이기 어렵고 조용히 쉬고 있다. 그러므로 정육면체는 고요와 안식을 뜻하며,
# > **어느 면(nodi)으로나 고르게 놓이고 움직이기 어렵다.**"
#
# 이 노트북은 리파의 논지를 **수치로 검증**한다. 다섯 정다면체와 구를 놓고
#
# 1. 면/꼭짓점/모서리 수
# 2. **구형도(sphericity)** — 얼마나 구에 가까운가(= 얼마나 굴러가기 쉬운가)
# 3. **넘어뜨리는 기울임 각도(tipping angle)** — 한 면으로 평면에 놓았을 때
#    무게중심이 접촉면 경계를 벗어나는 각도
# 4. **넘어뜨리는 데 드는 일(tipping work)** — 무게중심을 들어올려야 하는 높이
#
# 를 계산해 비교한다.
#
# 필요 패키지: numpy, plotly, kaleido (정적 이미지 저장용)

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


print("numpy", np.__version__)
# 출력: numpy 2.0.2

# %% [markdown]
# ## 1. 플라톤 『티마이오스』의 정다면체-원소 대응
#
# 『티마이오스』 53c–56c에서 플라톤은 네 원소에 네 개의 정다면체를 배당하고,
# 남은 하나(정십이면체)는 우주 전체(아이테르)에 맡긴다.
#
# | 정다면체 | 면 | 원소 | 배당 논거 |
# |---|---|---|---|
# | 정사면체 (tetrahedron) | 정삼각형 4 | **불** | 면·꼭짓점이 가장 적어 각이 가장 날카로움 → 찌르고 자름 |
# | 정팔면체 (octahedron) | 정삼각형 8 | **공기** | 중간 크기·중간 운동성 |
# | 정이십면체 (icosahedron) | 정삼각형 20 | **물** | 가장 둥글어 잘 흐르고 굴러감 |
# | 정육면체 (cube) | 정사각형 6 | **흙(대지)** | "가장 움직이기 어렵고(ἀκινητοτάτη) 가장 잘 빚어지며, **가장 안정된 바닥(βάσεις)** 을 가진 물체" (55d–e) |
# | 정십이면체 (dodecahedron) | 정오각형 12 | (우주 전체) | 남은 하나를 전체 우주에 배당 (55c) |
#
# 핵심 문장(55d–e): *"흙에는 정육면체 형태를 주자. 네 종류 중 흙이 가장
# 움직이기 어렵고 가장 잘 빚어지는 물체이며, 그런 성질을 가지려면 반드시
# 가장 안정된 바닥면을 가져야 하기 때문이다."*
#
# 즉 **정육면체 = 흙 = 부동(不動) = 고요**라는 연쇄가 여기서 나오고,
# 리파는 여기에 "대지는 우주의 중심에 있다"는 지구중심 우주론을 덧붙여
# **자기 자리에 있는 것은 움직이지 않는다**는 논거를 완성한다.

# %% [markdown]
# ## 2. 계산할 양의 정의
#
# 한 변 길이 $a$ 인 정다면체를 한 면으로 평면 위에 놓는다. 두 길이가 결정적이다.
#
# - **입체의 내접반경** $\rho$ : 중심(=무게중심)에서 면까지의 거리 = 바닥면 위 무게중심의 **높이**
# - **면의 내접반경(apothem)** $r_f$ : 면의 중심에서 모서리까지의 거리 = 무게중심이 넘어야 할 **수평 여유**
#
# 정 $n$ 각형 면의 apothem 은
#
# $$ r_f = \frac{a}{2\tan(\pi/n)} $$
#
# 무게중심을 접촉면의 한 모서리 위로 넘기려면 그 모서리를 축으로
#
# $$ \theta_{\text{tip}} = \arctan\!\left(\frac{r_f}{\rho}\right) $$
#
# 만큼 회전시켜야 한다. $\theta_{\text{tip}}$ 이 클수록 넘어뜨리기 어렵다.
# 이 값은 **크기에 무관**(scale-invariant)하다.
#
# 넘어뜨리는 동안 무게중심은 $\rho$ 에서 모서리까지의 거리
# $R_e = \sqrt{\rho^2 + r_f^2}$ 까지 올라가므로, 필요한 일은 단위무게당
#
# $$ \Delta h = \sqrt{\rho^2 + r_f^2} - \rho $$
#
# 이다. 부피가 다른 입체를 공평히 비교하려면 $\Delta h / V^{1/3}$ 로 정규화한다.
#
# 구형도(sphericity)는 같은 부피의 구 대비 표면적 비로
#
# $$ \Psi = \frac{\pi^{1/3}\,(6V)^{2/3}}{A} \qquad (\Psi = 1 \iff \text{구}) $$
#
# $\Psi$ 가 1에 가까울수록 구에 가깝고 = 굴러가기 쉽다.

# %%
S2, S3, S5, S6 = np.sqrt(2), np.sqrt(3), np.sqrt(5), np.sqrt(6)
a = 1.0  # 한 변 길이

SOLIDS = [
    # 이름, 면수 F, 꼭짓점 V, 모서리 E, 면의 각형 n, 내접반경 rho, 부피 V, 표면적 A
    dict(name="정사면체", en="tetrahedron", elem="불", F=4, Vt=4, E=6, n=3,
         rho=a / (2 * S6), vol=a**3 * S2 / 12, area=S3 * a**2),
    dict(name="정육면체", en="cube", elem="흙(대지)", F=6, Vt=8, E=12, n=4,
         rho=a / 2, vol=a**3, area=6 * a**2),
    dict(name="정팔면체", en="octahedron", elem="공기", F=8, Vt=6, E=12, n=3,
         rho=a / S6, vol=a**3 * S2 / 3, area=2 * S3 * a**2),
    dict(name="정십이면체", en="dodecahedron", elem="우주(아이테르)", F=12, Vt=20, E=30, n=5,
         rho=(a / 2) * np.sqrt(5 / 2 + 11 / (2 * S5)), vol=a**3 * (15 + 7 * S5) / 4,
         area=3 * np.sqrt(25 + 10 * S5) * a**2),
    dict(name="정이십면체", en="icosahedron", elem="물", F=20, Vt=12, E=30, n=3,
         rho=(a * S3 / 12) * (3 + S5), vol=a**3 * 5 * (3 + S5) / 12, area=5 * S3 * a**2),
]

for s in SOLIDS:
    s["r_f"] = a / (2 * np.tan(np.pi / s["n"]))                  # 면의 apothem
    s["tip_deg"] = np.degrees(np.arctan2(s["r_f"], s["rho"]))    # 기울임 각도
    s["dh"] = np.hypot(s["rho"], s["r_f"]) - s["rho"]            # 무게중심 상승량
    s["dh_norm"] = s["dh"] / s["vol"] ** (1 / 3)                 # 등부피 정규화
    s["psi"] = np.pi ** (1 / 3) * (6 * s["vol"]) ** (2 / 3) / s["area"]

# 구: 어떤 각도로도 무게중심이 접촉점 바로 위 → 기울임 각도 0
SPHERE = dict(name="구", en="sphere", elem="(포르투나의 천구)", F=np.inf, Vt=0, E=0,
              tip_deg=0.0, dh_norm=0.0, psi=1.0)

hdr = f"{'입체':<12}{'원소':<16}{'면':>4}{'꼭짓점':>7}{'모서리':>7}{'구형도Ψ':>9}{'기울임각(°)':>12}{'Δh/V^(1/3)':>13}"
print(hdr)
print("-" * len(hdr))
for s in SOLIDS + [SPHERE]:
    F = "∞" if s["F"] == np.inf else str(int(s["F"]))
    print(f"{s['name']:<12}{s['elem']:<16}{F:>4}{int(s['Vt']):>7}{int(s['E']):>7}"
          f"{s['psi']:>9.3f}{s['tip_deg']:>12.2f}{s['dh_norm']:>13.4f}")
# 출력:
# 입체          원소                 면    꼭짓점    모서리     구형도Ψ     기울임각(°)   Δh/V^(1/3)
# --------------------------------------------------------------------------------
# 정사면체        불                  4      4      6    0.671       54.74       0.3048
# 정육면체        흙(대지)              6      8     12    0.806       45.00       0.2071
# 정팔면체        공기                 8      6     12    0.846       35.26       0.1179
# 정십이면체       우주(아이테르)          12     20     30    0.910       31.72       0.0992
# 정이십면체       물                 20     12     30    0.939       20.91       0.0411
# 구           (포르투나의 천구)         ∞      0      0    1.000        0.00       0.0000
# (한글 폭 때문에 열이 어긋나 보이지만 값은 위와 같다)

# %% [markdown]
# ## 3. 읽어낸 결과
#
# ### (1) 리파가 옳은 부분 — 둥글어질수록 고요를 잃는다
#
# 구형도 $\Psi$ 와 기울임 각도는 **완벽한 역상관**이다.
#
# | | 정사면체 | 정육면체 | 정팔면체 | 정십이면체 | 정이십면체 | 구 |
# |---|---|---|---|---|---|---|
# | $\Psi$ | 0.671 | 0.806 | 0.846 | 0.910 | 0.939 | 1.000 |
# | $\theta_{\text{tip}}$ | 54.7° | **45.0°** | 35.3° | 31.7° | 20.9° | **0°** |
#
# 플라톤이 **물**에 준 정이십면체는 20.9°만 기울여도 넘어가고,
# **구**는 $\theta_{\text{tip}} = 0$ — 어떤 미세한 힘에도 굴러간다.
# 정육면체(45°)는 물의 정이십면체보다 **2배 이상** 넘어뜨리기 어렵고,
# 필요한 일($\Delta h/V^{1/3}$)로 보면 **5배** 차이가 난다.
#
# 르네상스 도상에서 **포르투나(운명)는 굴러가는 천구 위에 서고, 덕(Virtus)은
# 정육면체/네모난 좌석에 앉는다**는 대구가 바로 $\theta_{\text{tip}} = 0°$ 대
# $45°$ 의 대비다.
#
# ### (2) 리파의 논거가 흔들리는 지점 — 정사면체가 더 안 넘어진다
#
# 순수하게 '넘어뜨리기 어려움'만 재면 **정사면체가 54.7° 로 1위**다.
# 무게중심이 밑면 대비 매우 낮게 깔리기 때문이다. 그런데 플라톤은 정사면체를
# **불**에 배당했다. 논거가 '안정성'이 아니라 **날카로움**이었기 때문이다
# (면이 가장 적음 → 입체각이 가장 뾰족함 → 자르고 파고듦).
#
# ### (3) 그래서 정육면체의 진짜 특권 — "어느 면으로나 고르게(egualmente posato)"
#
# 리파의 문장에서 결정적인 것은 '가장 안 넘어진다'가 아니라 **등방성**이다.
# 정육면체만이 갖는 성질:
#
# - $r_f = \rho$ (= $a/2$) 인 **유일한** 정다면체 → $\theta_{\text{tip}}$ 이 정확히 $45°$.
#   받침 반폭과 무게중심 높이가 **같다**. 눕혀도 세워도 완전히 동일하다.
# - 서로 직교하는 **세 축의 길이가 같다** → 어떤 면을 바닥으로 골라도 같은 입체.
#   (정사면체는 밑면과 마주보는 것이 '점'이라 위아래가 다르다)
# - 정다면체 중 **혼자서 공간을 빈틈없이 채우는 유일한 입체** →
#   "우주의 중심을 메우고 있는 대지"라는 리파의 이미지에 정확히 대응.
#
# 즉 정육면체의 고요는 '가장 안 넘어짐'이 아니라 **어떻게 놓아도 똑같이 안정함**,
# 곧 움직일 이유가 없음이다.

# %%
names = [s["name"] for s in SOLIDS] + [SPHERE["name"]]
tips = [s["tip_deg"] for s in SOLIDS] + [SPHERE["tip_deg"]]
psis = [s["psi"] for s in SOLIDS] + [SPHERE["psi"]]
order = np.argsort(tips)[::-1]

BASE = "#8c7a5b"       # 판화 잉크/세피아
CUBE_C = "#b03a2e"     # 정육면체 강조
SPH_C = "#4a6fa5"      # 구
colors = []
for i in order:
    n = names[i]
    colors.append(CUBE_C if n == "정육면체" else (SPH_C if n == "구" else BASE))

fig = make_subplots(
    rows=1, cols=2, column_widths=[0.58, 0.42],
    specs=[[{"type": "xy"}, {"type": "scene"}]],
    subplot_titles=("한 면으로 놓았을 때 넘어뜨리는 기울임 각도 θ_tip",
                    "정육면체: r_f = ρ = a/2 → θ_tip = 45°"),
)

fig.add_bar(
    x=[names[i] for i in order], y=[tips[i] for i in order],
    marker_color=colors, marker_line_color="#3b3226", marker_line_width=1,
    text=[f"{tips[i]:.1f}°<br>Ψ={psis[i]:.3f}" for i in order],
    textposition="outside", textfont=dict(size=11),
    hovertemplate="%{x}<br>θ_tip = %{y:.2f}°<extra></extra>",
    name="θ_tip", showlegend=False, row=1, col=1,
)
fig.add_hline(y=45, line_dash="dot", line_color=CUBE_C, line_width=1.5,
              annotation_text="정육면체 45°", annotation_position="top left",
              row=1, col=1)
fig.update_yaxes(title_text="θ_tip (도)", range=[0, 66], row=1, col=1,
                 gridcolor="rgba(0,0,0,0.08)")
fig.update_xaxes(row=1, col=1)

# --- 오른쪽: 정육면체 3D 도해 (무게중심 · 받침 반폭 · 기울임 축) ---
c = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
              [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]], dtype=float)
faces = [(0, 1, 2), (0, 2, 3), (4, 5, 6), (4, 6, 7), (0, 1, 5), (0, 5, 4),
         (2, 3, 7), (2, 7, 6), (1, 2, 6), (1, 6, 5), (0, 3, 7), (0, 7, 4)]
fig.add_trace(go.Mesh3d(
    x=c[:, 0], y=c[:, 1], z=c[:, 2],
    i=[f[0] for f in faces], j=[f[1] for f in faces], k=[f[2] for f in faces],
    color="#d8cdb4", opacity=0.45, flatshading=True, hoverinfo="skip",
    showlegend=False), row=1, col=2)
edges = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4),
         (0, 4), (1, 5), (2, 6), (3, 7)]
ex, ey, ez = [], [], []
for i, j in edges:
    ex += [c[i, 0], c[j, 0], None]
    ey += [c[i, 1], c[j, 1], None]
    ez += [c[i, 2], c[j, 2], None]
fig.add_trace(go.Scatter3d(x=ex, y=ey, z=ez, mode="lines",
                           line=dict(color="#3b3226", width=3),
                           hoverinfo="skip", showlegend=False), row=1, col=2)
# 무게중심
fig.add_trace(go.Scatter3d(x=[0.5], y=[0.5], z=[0.5], mode="markers+text",
                           marker=dict(size=6, color=CUBE_C),
                           text=["무게중심 (높이 ρ=0.5)"], textposition="middle right",
                           textfont=dict(size=10), hoverinfo="skip",
                           showlegend=False), row=1, col=2)
# 무게중심 높이 ρ (수직) / 받침 반폭 r_f (수평)
fig.add_trace(go.Scatter3d(x=[0.5, 0.5], y=[0.5, 0.5], z=[0, 0.5], mode="lines",
                           line=dict(color=CUBE_C, width=5, dash="dash"),
                           hoverinfo="skip", showlegend=False), row=1, col=2)
fig.add_trace(go.Scatter3d(x=[0.5, 0.5], y=[0.5, 0.0], z=[0, 0], mode="lines+text",
                           line=dict(color=CUBE_C, width=5),
                           text=[None, "r_f=0.5"], textposition="bottom center",
                           textfont=dict(size=10), hoverinfo="skip",
                           showlegend=False), row=1, col=2)
# 기울임 축(밑면 모서리)
fig.add_trace(go.Scatter3d(x=[0, 1], y=[0, 0], z=[0, 0], mode="lines",
                           line=dict(color="#1a6b4a", width=8),
                           hoverinfo="skip", showlegend=False), row=1, col=2)
# 무게중심 → 기울임 모서리 (R_e)
fig.add_trace(go.Scatter3d(x=[0.5, 0.5], y=[0.5, 0.0], z=[0.5, 0.0], mode="lines",
                           line=dict(color="#1a6b4a", width=4, dash="dot"),
                           hoverinfo="skip", showlegend=False), row=1, col=2)

fig.update_scenes(
    xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
    aspectmode="cube", camera=dict(eye=dict(x=1.7, y=-1.7, z=1.0)),
    row=1, col=2,
)
fig.update_layout(
    title=dict(text="리파 『이코놀로지아』 Quiete — 정육면체가 '고요'인 이유의 수치화",
               x=0.5, xanchor="center", font=dict(size=17)),
    template="plotly_white", paper_bgcolor="#faf7f0", plot_bgcolor="#faf7f0",
    width=1180, height=560, margin=dict(l=60, r=30, t=95, b=60),
    font=dict(family="AppleGothic, Apple SD Gothic Neo, Malgun Gothic, sans-serif",
              size=12, color="#2b2b2b"),
)

_show(fig)
fig.write_image("expy.png", scale=2)
print("saved expy.png")
# 출력: saved expy.png

# %% [markdown]
# ## 4. 다림추(perpendicolo)까지 — 리파의 두 번째 상징
#
# 리파는 여인의 오른손에 **다림추(perpendicolo, plumb bob)** 를 들린다. 그 설명:
#
# > "다림추는 모든 것의 고요와 안식이 그것들의 **목적이자 완성**임을 보여준다.
# > 다림추는 무겁고 자기 자리 밖에 있으므로 곧게 매달려, 자연히 움직여
# > 지평의 한 점에 이르려 한다 — 거기가 그것의 고요다."
#
# 즉 다림추는 **"운동은 정지를 목표로 한다"** 는 아리스토텔레스적 자연운동론의
# 도상이다. 무거운 것은 자기 자연적 장소(우주 중심 = 대지)로 향하고,
# 그 자리에 닿으면 멈춘다. 정육면체(=대지=목표점)와 다림추(=목표를 향한 운동)는
# 한 논증의 결론과 과정인 셈이다.
#
# 리파는 이어서 냉정하게 덧붙인다: 이 세상에는 참된 고요가 없다 —
# 단순 원소들조차 생성·소멸하고 천체는 영구 운동 중이므로, 우리는 고요를
# 감각으로 확인하지 못하고 **지성으로 상상할 뿐**이다. 인간의 고요는
# 생각과 행동의 운동이 올바르게 정렬되어 그 안식처, 곧 내세로 향할 때 성립한다.
#
# 수치 요약: 정육면체의 $\theta_{\text{tip}} = 45°$ 는 절대적 부동이 아니라
# **유한하지만 등방적인 안정**이다. 이 세상에서 얻을 수 있는 고요의 정확한 크기가
# 45도라는 것 — 리파의 결론과 잘 맞아떨어진다.
