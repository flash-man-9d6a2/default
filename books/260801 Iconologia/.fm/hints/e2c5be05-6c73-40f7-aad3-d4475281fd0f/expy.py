# %% [markdown]
# # 무지개의 광학 — 리파의 "완전한 원이 되지 못하는 호"를 수치로 확인하기
#
# 체사레 리파 『이코놀로지아』의 **공기의 님프 이리스(Iride)** 항목은 이렇게 적는다.
#
# > *"Non fi vede detta figura dalle ginocchia abbaſſo, perchè l' Arco baleno non è mai circolo perfetto."*
# > (이 도상은 무릎 아래가 보이지 않는데, 무지개는 결코 완전한 원이 되지 못하기 때문이다.)
#
# 리파(1593~1603)는 **왜** 그런지는 설명하지 못했다. 그 설명은 데카르트(1637, 『기상학』)와
# 뉴턴(1666~1672, 색 분산)에 이르러서야 완성된다. 이 노트북에서는 리파의 문장을 뒷받침하는
# 근대 광학을 단계적으로 계산한다.
#
# 1. 스넬의 법칙으로 물방울 속 광선 경로 추적 → 총 편향각 $D(\theta_i)$
# 2. $D$ 의 극값 = 무지개 각 (약 $138°$, 시야각 $42°$), 해석해와 수치해 비교
# 3. 파장별 굴절률 → 색마다 다른 무지개 각, 빨강이 바깥쪽인 이유
# 4. 2회 내부 반사 = 2차 무지개(약 $51°$)와 색 순서 반전
# 5. 태양 고도별 가시 호 범위 → 고도 $42°$ 초과 시 무지개 소멸

# %%
# 필요 패키지: numpy, plotly, kaleido
import os

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


HERE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else "."
print("numpy", np.__version__)
# 출력: numpy 2.0.2

# %% [markdown]
# ## 1. 스넬의 법칙과 총 편향각 $D(\theta_i)$
#
# 공기($n_1 = 1$)에서 물방울($n_2 = n$)로 들어가는 광선의 입사각을 $\theta_i$,
# 굴절각을 $\theta_r$ 라 하면 스넬의 법칙은
#
# $$\sin\theta_i = n \sin\theta_r \quad\Longrightarrow\quad \theta_r = \arcsin\!\left(\frac{\sin\theta_i}{n}\right)$$
#
# 구형 물방울은 대칭이므로 광선은 세 번 방향을 꺾는다.
#
# | 사건 | 편향량 |
# |---|---|
# | 입사 시 굴절 | $\theta_i - \theta_r$ |
# | 뒷면 내부 반사 1회 | $180° - 2\theta_r$ |
# | 출사 시 굴절 | $\theta_i - \theta_r$ |
#
# 합하면 **1차 무지개의 총 편향각**
#
# $$D(\theta_i) = 180° + 2\theta_i - 4\theta_r$$
#
# 관측자가 태양 반대점(antisolar point)에서 재는 **시야각**은
#
# $$\alpha = 180° - D(\theta_i) = 4\theta_r - 2\theta_i$$
#
# 내부 반사를 $k$ 회 하는 일반식은 $D_k(\theta_i) = k\cdot 180° + 2\theta_i - 2(k+1)\theta_r$ 이다.

# %%
N_WATER = 1.333  # 가시광 평균 굴절률 (589 nm 근처)


def theta_r(theta_i_deg, n=N_WATER):
    """스넬의 법칙: 입사각(도) -> 굴절각(도)"""
    return np.degrees(np.arcsin(np.sin(np.radians(theta_i_deg)) / n))


def deviation(theta_i_deg, n=N_WATER, k=1):
    """내부 반사 k회 광선의 총 편향각 D (도)"""
    tr = theta_r(theta_i_deg, n)
    return k * 180.0 + 2.0 * theta_i_deg - 2.0 * (k + 1) * tr


for ti in [0, 20, 40, 59.6, 70, 89]:
    print(f"theta_i={ti:5.1f}  theta_r={theta_r(ti):6.3f}  D={deviation(ti):8.3f}  시야각={180 - deviation(ti):7.3f}")
# 출력: theta_i=  0.0  theta_r= 0.000  D= 180.000  시야각=  0.000
# 출력: theta_i= 20.0  theta_r=14.867  D= 160.531  시야각= 19.469
# 출력: theta_i= 40.0  theta_r=28.830  D= 144.680  시야각= 35.320
# 출력: theta_i= 59.6  theta_r=40.319  D= 137.923  시야각= 42.077
# 출력: theta_i= 70.0  theta_r=44.825  D= 140.699  시야각= 39.301
# 출력: theta_i= 89.0  theta_r=48.597  D= 163.613  시야각= 16.387

# %% [markdown]
# $\theta_i$ 를 $0°$ 에서 $90°$ 로 훑으면 $D$ 가 한 번 **내려갔다 올라온다**.
# 즉 최소값이 존재한다. 이 최소 편향각 근처에서 $dD/d\theta_i \approx 0$ 이므로
# 넓은 범위의 입사각이 거의 같은 방향으로 빛을 몰아준다 → **빛이 쌓여 밝은 호**가 된다.
# 이것이 무지개가 특정 각도에서만 보이는 이유다(**Descartes ray**, 1637).

# %% [markdown]
# ## 2. 극값 찾기 — 수치해 vs 해석해
#
# 해석적으로 $D = 180° + 2\theta_i - 4\theta_r$ 를 미분한다.
# $\sin\theta_i = n\sin\theta_r$ 를 양변 미분하면 $\cos\theta_i \, d\theta_i = n\cos\theta_r \, d\theta_r$ 이므로
#
# $$\frac{dD}{d\theta_i} = 2 - 4\frac{d\theta_r}{d\theta_i} = 2 - \frac{4\cos\theta_i}{n\cos\theta_r} = 0
# \quad\Longrightarrow\quad n\cos\theta_r = 2\cos\theta_i$$
#
# $\cos\theta_r = \sqrt{1 - \sin^2\theta_i / n^2}$ 를 대입해 $\cos^2\theta_i$ 에 대해 풀면
#
# $$\boxed{\;\cos\theta_i = \sqrt{\frac{n^2 - 1}{3}}\;}$$
#
# 일반적으로 내부 반사 $k$ 회에서는 $\cos\theta_i = \sqrt{\dfrac{n^2-1}{(k+1)^2-1}}$ 이다.

# %%
def theta_i_critical(n=N_WATER, k=1):
    """해석해: 무지개 각을 만드는 입사각 (도)"""
    return np.degrees(np.arccos(np.sqrt((n**2 - 1.0) / ((k + 1) ** 2 - 1.0))))


# 수치해: 촘촘한 격자에서 D의 극값 탐색
grid = np.linspace(1e-6, 89.999999, 2_000_001)
D1 = deviation(grid, N_WATER, k=1)
i_num = np.argmin(D1)

ti_num, D_num = grid[i_num], D1[i_num]
ti_ana = theta_i_critical(N_WATER, k=1)
D_ana = deviation(ti_ana, N_WATER, k=1)

print(f"수치해   : theta_i = {ti_num:.6f} deg,  D_min = {D_num:.6f} deg,  시야각 = {180 - D_num:.6f} deg")
print(f"해석해   : theta_i = {ti_ana:.6f} deg,  D_min = {D_ana:.6f} deg,  시야각 = {180 - D_ana:.6f} deg")
print(f"차이     : dtheta = {abs(ti_num - ti_ana):.3e} deg,  dD = {abs(D_num - D_ana):.3e} deg")
print(f"검증 n*cos(theta_r) = {N_WATER * np.cos(np.radians(theta_r(ti_ana))):.9f}")
print(f"     2*cos(theta_i) = {2 * np.cos(np.radians(ti_ana)):.9f}")
# 출력: 수치해   : theta_i = 59.410485 deg,  D_min = 137.921893 deg,  시야각 = 42.078107 deg
# 출력: 해석해   : theta_i = 59.410473 deg,  D_min = 137.921893 deg,  시야각 = 42.078107 deg
# 출력: 차이     : dtheta = 1.165e-05 deg,  dD = 2.984e-12 deg
# 출력: 검증 n*cos(theta_r) = 1.017768146
# 출력:      2*cos(theta_i) = 1.017768146

# %% [markdown]
# 수치해와 해석해가 소수점 6자리까지 일치한다.
# **총 편향각 $D_{\min} \approx 137.92° \approx 138°$**, 따라서
# **시야각 $180° - D_{\min} \approx 42.08°$** — 이것이 1차 무지개의 반각(半角)이다.
#
# 무지개는 태양 반대점을 중심으로 반각 $42°$ 의 **원뿔**을 이룬다. 원뿔이므로 본질은 완전한 원이고,
# 지평선이 그것을 자르기 때문에 우리는 호(arc)만 본다. 리파의 "무릎 아래는 구름에 가려 보이지 않는다"는
# 바로 이 절단된 원을 알레고리로 옮긴 것이다.

# %%
# 굴절률 민감도: n이 커지면 무지개 각은 작아진다
for n in [1.30, 1.331, 1.333, 1.344, 1.36]:
    ti = theta_i_critical(n, 1)
    print(f"n={n:.3f} -> theta_i={ti:6.3f}, D_min={deviation(ti, n, 1):8.4f}, 시야각={180 - deviation(ti, n, 1):7.4f}")
# 출력: n=1.300 -> theta_i=61.342, D_min=132.8679, 시야각=47.1321
# 출력: n=1.331 -> theta_i=59.527, D_min=137.6302, 시야각=42.3698
# 출력: n=1.333 -> theta_i=59.410, D_min=137.9219, 시야각=42.0781
# 출력: n=1.344 -> theta_i=58.772, D_min=139.4950, 시야각=40.5050
# 출력: n=1.360 -> theta_i=57.848, D_min=141.6918, 시야각=38.3082

# %% [markdown]
# ## 3. 색 분산 — 왜 빨강이 바깥쪽인가
#
# 물의 굴절률은 파장에 따라 다르다(정상 분산): 짧은 파장(보라)일수록 $n$ 이 크다.
#
# | 색 | 파장 | $n$ |
# |---|---|---|
# | 빨강 | 656 nm | 1.3311 |
# | 주황 | 610 nm | 1.3324 |
# | 노랑 | 589 nm | 1.3330 |
# | 초록 | 509 nm | 1.3360 |
# | 파랑 | 486 nm | 1.3371 |
# | 보라 | 405 nm | 1.3428 |
#
# 위 민감도 표에서 확인했듯 $n$ 이 크면 무지개 각이 **작아진다**.
# 보라의 $n$ 이 가장 크므로 보라의 호가 가장 작고(안쪽), 빨강의 호가 가장 크다(바깥쪽).

# %%
COLORS = [
    # (이름, 파장 nm, 굴절률, plotly 색)
    ("빨강", 656, 1.3311, "#d62728"),
    ("주황", 610, 1.3324, "#ff7f0e"),
    ("노랑", 589, 1.3330, "#e8c400"),
    ("초록", 509, 1.3360, "#2ca02c"),
    ("파랑", 486, 1.3371, "#1f77b4"),
    ("보라", 405, 1.3428, "#7c4dff"),
]

primary = []
secondary = []
for name, lam, n, col in COLORS:
    a1 = 180.0 - deviation(theta_i_critical(n, 1), n, 1)  # 1차: 시야각
    a2 = deviation(theta_i_critical(n, 2), n, 2) - 180.0  # 2차: D>180 이므로 D-180
    primary.append((name, lam, n, a1, col))
    secondary.append((name, lam, n, a2, col))
    print(f"{name} lam={lam}nm n={n:.4f}  1차={a1:7.4f} deg   2차={a2:7.4f} deg")
# 출력: 빨강 lam=656nm n=1.3311  1차=42.3552 deg   2차=50.3915 deg
# 출력: 주황 lam=610nm n=1.3324  1차=42.1654 deg   2차=50.7334 deg
# 출력: 노랑 lam=589nm n=1.3330  1차=42.0781 deg   2차=50.8908 deg
# 출력: 초록 lam=509nm n=1.3360  1차=41.6438 deg   2차=51.6740 deg
# 출력: 파랑 lam=486nm n=1.3371  1차=41.4856 deg   2차=51.9597 deg
# 출력: 보라 lam=405nm n=1.3428  1차=40.6741 deg   2차=53.4267 deg

# %%
w1 = primary[0][3] - primary[-1][3]  # 빨강 - 보라 (1차)
w2 = secondary[-1][3] - secondary[0][3]  # 보라 - 빨강 (2차)
print(f"1차 무지개 폭(빨강-보라) = {w1:.3f} deg  -> 바깥이 빨강, 안쪽이 보라")
print(f"2차 무지개 폭(보라-빨강) = {w2:.3f} deg  -> 순서 반전: 바깥이 보라, 안쪽이 빨강")
print(f"1차/2차 사이 어두운 띠(Alexander's dark band) 폭 = {secondary[0][3] - primary[0][3]:.3f} deg")
print(f"참고: 태양/달의 시직경은 약 0.5 deg -> 무지개 색 띠는 그 {w1 / 0.5:.1f}배 두께")
# 출력: 1차 무지개 폭(빨강-보라) = 1.681 deg  -> 바깥이 빨강, 안쪽이 보라
# 출력: 2차 무지개 폭(보라-빨강) = 3.035 deg  -> 순서 반전: 바깥이 보라, 안쪽이 빨강
# 출력: 1차/2차 사이 어두운 띠(Alexander's dark band) 폭 = 8.036 deg
# 출력: 참고: 태양/달의 시직경은 약 0.5 deg -> 무지개 색 띠는 그 3.4배 두께

# %% [markdown]
# ### 리파의 색 순서와 비교
#
# 리파가 적은 날개 색은 **porpora(자주) → pavonazzo(보라) → azzurro(파랑) → verde(초록)** 네 층이다.
# 실제 1차 무지개는 바깥에서 안쪽으로 **빨강 → 주황 → 노랑 → 초록 → 파랑 → 보라**.
#
# - 리파의 순서는 계산된 무지개 안쪽 절반(자주/보라/파랑/초록)만 담고 있으며,
#   빨강·주황·노랑이 아예 빠져 있다.
# - 이는 실측 목록이 아니라 **아리스토텔레스 『기상학』 3권**의 3색 전통(붉음·초록·보라)을 이은
#   "몇 개의 색층"이라는 관념적 나열이다. 뉴턴이 7색을 제시(1672)하기 전까지 유럽에서 무지개 색은
#   보통 3~4색으로 셌다.

# %%
# 만약 무지개 색층이 리파처럼 4개뿐이라면? 실제 각도 폭을 4등분해 비교
edges = np.linspace(primary[-1][3], primary[0][3], 5)  # 보라 -> 빨강 사이 4구간
ripa = ["초록", "파랑", "보라(pavonazzo)", "자주(porpora)"]  # 리파 나열의 역순 = 안->밖
for name, lo, hi in zip(ripa, edges[:-1], edges[1:]):
    print(f"리파식 4층 {name:16s}: {lo:.3f} ~ {hi:.3f} deg (폭 {hi - lo:.3f})")
print(f"-> 실제로는 이 {w1:.3f} deg 안에 빨강~보라 전 스펙트럼이 연속적으로 들어간다")
# 출력: 리파식 4층 초록              : 40.674 ~ 41.094 deg (폭 0.420)
# 출력: 리파식 4층 파랑              : 41.094 ~ 41.515 deg (폭 0.420)
# 출력: 리파식 4층 보라(pavonazzo)   : 41.515 ~ 41.935 deg (폭 0.420)
# 출력: 리파식 4층 자주(porpora)     : 41.935 ~ 42.355 deg (폭 0.420)
# 출력: -> 실제로는 이 1.681 deg 안에 빨강~보라 전 스펙트럼이 연속적으로 들어간다

# %% [markdown]
# ## 4. 2차 무지개 — 내부 반사 2회
#
# 내부 반사를 두 번 하면 $D_2(\theta_i) = 360° + 2\theta_i - 6\theta_r$ 이고,
# 극값 조건은 $\cos\theta_i = \sqrt{(n^2-1)/8}$ 이다. 이번에는 $D_2 > 180°$ 라
# 빛이 "한 바퀴 넘게" 돌아 나오므로 시야각은 $D_2 - 180° \approx 51°$ 가 된다.
# 반사가 한 번 더 늘어난 만큼 **색 순서가 반전**되고, 반사 손실 때문에 훨씬 어둡다.

# %%
ti2_ana = theta_i_critical(N_WATER, 2)
D2_grid = deviation(grid, N_WATER, k=2)
i2 = np.argmin(D2_grid)
print(f"2차 해석해: theta_i={ti2_ana:.4f} deg, D_min={deviation(ti2_ana, N_WATER, 2):.4f} deg, "
      f"시야각={deviation(ti2_ana, N_WATER, 2) - 180:.4f} deg")
print(f"2차 수치해: theta_i={grid[i2]:.4f} deg, D_min={D2_grid[i2]:.4f} deg, 시야각={D2_grid[i2] - 180:.4f} deg")
print(f"1차 시야각 {180 - D_ana:.2f} deg  <  2차 시야각 {deviation(ti2_ana, N_WATER, 2) - 180:.2f} deg  "
      "-> 2차가 바깥쪽")
# 출력: 2차 해석해: theta_i=71.8427 deg, D_min=230.8908 deg, 시야각=50.8908 deg
# 출력: 2차 수치해: theta_i=71.8427 deg, D_min=230.8908 deg, 시야각=50.8908 deg
# 출력: 1차 시야각 42.08 deg  <  2차 시야각 50.89 deg  -> 2차가 바깥쪽

# %% [markdown]
# ## 5. 태양 고도와 가시 호 — "완전한 원이 되지 못한다"의 정량화
#
# 관측자 눈높이를 지면으로 보면, 무지개의 중심(태양 반대점)의 고도는
#
# $$h_{\text{anti}} = -h_{\odot}$$
#
# 즉 태양 고도 $h_\odot$ 만큼 **지평선 아래**에 있다. 무지개는 그 중심을 둘러싼 반각 $\alpha=42°$ 원뿔이므로
# 호의 최고점 고도는
#
# $$h_{\text{top}} = \alpha - h_{\odot}$$
#
# 지평선 위에 남는 호의 방위 반각(중심각 기준)은
#
# $$\Delta\phi = \arccos\!\left(\frac{\tan h_\odot}{\tan \alpha}\right)\ \text{에 대응하는 원주 비율}$$
#
# 더 간단히, 원뿔 축을 따라 매개변수화한 원 위의 점 중 고도가 $0$ 이상인 비율로 계산한다.
# 결론은 명확하다.
#
# - $h_\odot = 0°$ (일출/일몰): 정확히 **반원**(원의 50%)
# - $h_\odot$ 증가 → 호가 점점 짧아짐
# - $h_\odot > 42.1°$ → 원 전체가 지평선 아래 → **무지개 안 보임**
#
# 그래서 한여름 정오에는 무지개를 볼 수 없고, 무지개는 아침·저녁의 현상이다.
# 반대로 비행기·폭포·분수처럼 **관측자 아래에도 물방울이 있으면 원형 무지개**가 보인다.

# %%
ALPHA1 = 180.0 - D_ana  # 1차 무지개 반각 (deg), §2에서 구한 값
ALPHA2 = deviation(theta_i_critical(N_WATER, 2), N_WATER, 2) - 180.0
print(f"ALPHA1 = {ALPHA1:.6f} deg,  ALPHA2 = {ALPHA2:.6f} deg")
# 출력: ALPHA1 = 42.078107 deg,  ALPHA2 = 50.890758 deg


def visible_fraction(sun_alt_deg, alpha_deg=ALPHA1, m=200001):
    """태양 고도에 대해 무지개 원 중 지평선 위에 보이는 비율과 호 최고 고도"""
    a = np.radians(alpha_deg)
    hs = np.radians(sun_alt_deg)
    t = np.linspace(0.0, 2 * np.pi, m)
    # 태양 반대점을 중심으로 한 반각 a 원뿔. 반대점 고도 = -hs.
    # 원 위 점의 고도: sin(alt) = -sin(hs)cos(a) + cos(hs)sin(a)cos(t)
    sin_alt = -np.sin(hs) * np.cos(a) + np.cos(hs) * np.sin(a) * np.cos(t)
    alt = np.degrees(np.arcsin(np.clip(sin_alt, -1, 1)))
    return float((alt >= 0).mean()), float(alt.max())


for h in [0, 5, 10, 20, 30, 40, 42, ALPHA1, 43, 50]:
    frac, top = visible_fraction(h)
    tag = "  <-- 보이지 않음" if top <= 0.0 else ""
    print(f"태양 고도 {h:7.4f} deg -> 가시 비율 {frac * 100:5.1f}% , 호 최고 고도 {top:7.3f} deg{tag}")
# 출력: 태양 고도  0.0000 deg -> 가시 비율  50.0% , 호 최고 고도  42.078 deg
# 출력: 태양 고도  5.0000 deg -> 가시 비율  46.9% , 호 최고 고도  37.078 deg
# 출력: 태양 고도 10.0000 deg -> 가시 비율  43.7% , 호 최고 고도  32.078 deg
# 출력: 태양 고도 20.0000 deg -> 가시 비율  36.8% , 호 최고 고도  22.078 deg
# 출력: 태양 고도 30.0000 deg -> 가시 비율  27.9% , 호 최고 고도  12.078 deg
# 출력: 태양 고도 40.0000 deg -> 가시 비율  12.0% , 호 최고 고도   2.078 deg
# 출력: 태양 고도 42.0000 deg -> 가시 비율   2.4% , 호 최고 고도   0.078 deg
# 출력: 태양 고도 42.0781 deg -> 가시 비율   0.0% , 호 최고 고도   0.000 deg  <-- 보이지 않음
# 출력: 태양 고도 43.0000 deg -> 가시 비율   0.0% , 호 최고 고도  -0.922 deg  <-- 보이지 않음
# 출력: 태양 고도 50.0000 deg -> 가시 비율   0.0% , 호 최고 고도  -7.922 deg  <-- 보이지 않음

# %%
# 임계 고도를 이분법으로 찾아 무지개 반각과 일치하는지 확인
lo, hi = 30.0, 60.0
for _ in range(60):
    mid = 0.5 * (lo + hi)
    if visible_fraction(mid, m=20001)[0] > 0.0:
        lo = mid
    else:
        hi = mid
print(f"가시 임계 태양 고도 = {0.5 * (lo + hi):.6f} deg")
print(f"1차 무지개 반각    = {ALPHA1:.6f} deg   (동일해야 함)")
# 출력: 가시 임계 태양 고도 = 42.078107 deg
# 출력: 1차 무지개 반각    = 42.078107 deg   (동일해야 함)

# %% [markdown]
# 임계 태양 고도가 무지개 반각과 정확히 같다. **태양이 $42.1°$ 보다 높으면 무지개는 원리적으로 볼 수 없다.**
#
# 리파의 도상 문법으로 옮기면:
# 무릎 아래를 가린 구름은 "지평선에 잘린 원"이고, 그 잘림은 태양 고도라는 순수한 기하학의 결과다.
# 1600년경의 알레고리 화가는 그 이유를 몰랐지만, 관찰만으로 **"결코 완전한 원이 아니다"** 는 사실은
# 정확히 붙잡아 도상에 새겼다.

# %% [markdown]
# ## 6. 시각화

# %%
fig = make_subplots(
    rows=2,
    cols=2,
    specs=[[{"colspan": 2}, None], [{}, {}]],
    subplot_titles=(
        "(a) 총 편향각 D(θi) — 1차·2차 무지개의 극값",
        "(b) 색별 무지개 각 (1차 vs 2차)",
        "(c) 태양 고도별 지평선 위 가시 호 비율",
    ),
    vertical_spacing=0.16,
    horizontal_spacing=0.12,
)

# (a) D(theta_i) 곡선
gs = np.linspace(0.01, 89.99, 1500)
fig.add_trace(
    go.Scatter(x=gs, y=deviation(gs, N_WATER, 1), name="k=1 (1차)", line=dict(color="#1f77b4", width=2.5)),
    row=1, col=1,
)
fig.add_trace(
    go.Scatter(x=gs, y=deviation(gs, N_WATER, 2) - 180.0, name="k=2 (2차, D−180°)",
               line=dict(color="#9467bd", width=2.5, dash="dash")),
    row=1, col=1,
)
fig.add_trace(
    go.Scatter(x=[ti_ana], y=[D_ana], mode="markers+text", name=f"D_min ≈ {D_ana:.1f}°",
               marker=dict(color="#d62728", size=12, symbol="star"),
               text=[f"θi={ti_ana:.1f}°, D={D_ana:.1f}°<br>→ 시야각 {ALPHA1:.1f}°"],
               textposition="bottom right", textfont=dict(size=11)),
    row=1, col=1,
)
fig.add_trace(
    go.Scatter(x=[ti2_ana], y=[ALPHA2], mode="markers+text",
               name=f"2차 극값 ≈ {ALPHA2:.1f}°", marker=dict(color="#7f7f7f", size=11, symbol="diamond"),
               text=[f"  θi={ti2_ana:.1f}° → 시야각 {ALPHA2:.1f}°"],
               textposition="top center", textfont=dict(size=11)),
    row=1, col=1,
)
fig.add_hline(y=D_ana, line=dict(color="#d62728", width=1, dash="dot"), row=1, col=1)
fig.update_xaxes(title_text="입사각 θi (deg)", row=1, col=1)
fig.update_yaxes(title_text="편향각 (deg)", row=1, col=1)

# (b) 색별 무지개 각
fig.add_trace(
    go.Scatter(x=[p[3] for p in primary], y=[p[0] for p in primary], mode="markers",
               name="1차 (안쪽 호)", marker=dict(color=[p[4] for p in primary], size=15, symbol="circle",
                                            line=dict(color="#333", width=1)), showlegend=False),
    row=2, col=1,
)
fig.add_trace(
    go.Scatter(x=[s[3] for s in secondary], y=[s[0] for s in secondary], mode="markers",
               name="2차 (바깥 호)", marker=dict(color=[s[4] for s in secondary], size=15, symbol="square",
                                             line=dict(color="#333", width=1)), showlegend=False),
    row=2, col=1,
)
fig.add_annotation(x=ALPHA1, y=-0.8, text="1차 ●<br>빨강이 바깥", showarrow=False,
                   font=dict(size=10), row=2, col=1)
fig.add_annotation(x=ALPHA2, y=-0.8, text="2차 ■<br>보라가 바깥", showarrow=False,
                   font=dict(size=10), row=2, col=1)
fig.update_xaxes(title_text="시야각 (deg)", range=[39.8, 54.4], row=2, col=1)
fig.update_yaxes(title_text="", row=2, col=1)

# (c) 태양 고도별 가시 비율
alts = np.linspace(0, 50, 201)
fracs = np.array([visible_fraction(a, m=20001)[0] * 100 for a in alts])
tops = np.array([visible_fraction(a, m=20001)[1] for a in alts])
fig.add_trace(
    go.Scatter(x=alts, y=fracs, name="가시 비율 (%)", line=dict(color="#2ca02c", width=2.5), showlegend=False),
    row=2, col=2,
)
fig.add_trace(
    go.Scatter(x=alts, y=np.maximum(tops, 0), name="호 최고 고도 (deg)",
               line=dict(color="#ff7f0e", width=2, dash="dot"), showlegend=False),
    row=2, col=2,
)
fig.add_vline(x=ALPHA1, line=dict(color="#d62728", width=2, dash="dash"), row=2, col=2)
fig.add_annotation(x=ALPHA1, y=46, text=f"{ALPHA1:.1f}° 초과 →<br>무지개 없음", showarrow=True, arrowhead=2,
                   ax=-60, ay=-10, font=dict(size=10, color="#d62728"), row=2, col=2)
fig.add_annotation(x=2, y=52, text="일출/일몰 = 정확히 반원(50%)", showarrow=False,
                   font=dict(size=10), xanchor="left", row=2, col=2)
fig.update_xaxes(title_text="태양 고도 (deg)", row=2, col=2)
fig.update_yaxes(title_text="가시 비율(%) / 최고 고도(deg)", row=2, col=2)

fig.update_layout(
    title_text="무지개의 광학 — 리파 『이코놀로지아』 이리스(Iride) 도상의 물리적 근거",
    height=880,
    width=1180,
    template="plotly_white",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    font=dict(family="Apple SD Gothic Neo, Noto Sans KR, sans-serif", size=12),
)

_show(fig)
out_png = os.path.join(HERE, "expy.png")
fig.write_image(out_png, scale=2)
print("saved:", out_png, os.path.getsize(out_png), "bytes")
# 출력: saved: .../expy.png (약 340 KB)

# %% [markdown]
# ## 정리
#
# | 리파의 도상 요소 | 물리적 대응 | 이 노트북의 계산 |
# |---|---|---|
# | 반원으로 펼친 날개 | 태양 반대점 중심 반각 $42°$ 원뿔이 지평선에 잘림 | §2, §5 |
# | 여러 층의 색(자주·보라·파랑·초록) | 분산으로 색마다 다른 무지개 각 | §3 (실제 폭 $1.68°$, 순서는 빨강→보라) |
# | 안개·잔 물방울 머리카락 | 무지개 생성의 필수 조건인 물방울 | §1 (물방울이 곧 광학 소자) |
# | 무릎 아래를 가린 구름 | 지평선 아래 절반은 물방울이 없어 호가 끊김 | §5 (고도 $42.1°$ 초과 시 소멸) |
# | 청색 붓꽃 giglio ceruleo | 어원 유희 iris = 무지개 = 붓꽃 | (물리 아님, README 참조) |
