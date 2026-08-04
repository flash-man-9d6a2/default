# %% [markdown]
# # 리파의 '달(月)' 정의를 수치로 검증하기
#
# 필요 패키지: `numpy`, `plotly`, `kaleido`
#
# 리파는 『Iconologia』의 「Mese in Generale」에서 달(月)을 이렇게 정의한다.
#
# > "달(月)이란 **달(Luna)이 황도 12궁을 도는 여정**에 다름 아니며,
# > 그 여정 동안 우리 눈에는 일부는 차고 일부는 기우는 것처럼 보인다."
#
# 이 한 문장에는 **서로 다른 두 주기**가 붙어 있다.
#
# | 리파의 문구 | 실제 주기 | 값 |
# |---|---|---|
# | "12궁을 도는 여정" | 항성월 $T_{sid}$ | 27.32166일 |
# | "차고 기움" | 삭망월 $T_{syn}$ | 29.53059일 |
#
# 이 노트북에서 두 값이 왜 다르고 얼마나 어긋나는지 직접 계산·시각화한다.

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


# 천문 상수 (일 단위)
T_SID = 27.32166  # 항성월: 항성(=12궁) 기준 공전 주기
T_YR = 365.2564  # 항성년: 지구의 항성 기준 공전 주기
T_SYN_OBS = 29.530589  # 삭망월 관측값 (신월→신월)
T_TROP_YR = 365.2422  # 태양년(춘분점 기준)

print(f"항성월 T_sid = {T_SID} 일")
print(f"항성년 T_yr  = {T_YR} 일")
print(f"삭망월 관측값 T_syn = {T_SYN_OBS} 일")
# 출력:
# 항성월 T_sid = 27.32166 일
# 항성년 T_yr  = 365.2564 일
# 삭망월 관측값 T_syn = 29.530589 일

# %% [markdown]
# ## 1. 회합주기 공식으로 삭망월 유도
#
# 달의 각속도에서 지구의 공전 각속도를 빼면, **태양에 대한** 달의 상대 각속도가 나온다.
# 위상은 태양–지구–달 이각으로 결정되므로 위상 주기는 이 상대 각속도의 주기다.
#
# $$\frac{1}{T_{\text{syn}}} = \frac{1}{T_{\text{sid}}} - \frac{1}{T_{\text{yr}}}$$

# %%
inv_syn = 1.0 / T_SID - 1.0 / T_YR
T_syn = 1.0 / inv_syn

print(f"1/T_sid = {1 / T_SID:.8f} rev/day")
print(f"1/T_yr  = {1 / T_YR:.8f} rev/day")
print(f"차이    = {inv_syn:.8f} rev/day")
print()
print(f"유도된 삭망월  T_syn = {T_syn:.6f} 일")
print(f"관측 삭망월          = {T_SYN_OBS:.6f} 일")
print(f"오차                 = {T_syn - T_SYN_OBS:+.6f} 일 ({(T_syn - T_SYN_OBS) * 24 * 60:+.2f} 분)")
print(f"상대오차             = {abs(T_syn - T_SYN_OBS) / T_SYN_OBS * 100:.4f} %")
print()
print(f"항성월과의 차이 = {T_syn - T_SID:.4f} 일")
# 출력:
# 1/T_sid = 0.03660100 rev/day
# 1/T_yr  = 0.00273780 rev/day
# 차이    = 0.03386319 rev/day
#
# 유도된 삭망월  T_syn = 29.530587 일
# 관측 삭망월          = 29.530589 일
# 오차                 = -0.000002 일 (-0.00 분)
# 상대오차             = 0.0000 %
#
# 항성월과의 차이 = 2.2089 일

# %% [markdown]
# 공식이 관측값을 **분 단위 이하**로 재현한다. 차이 2.21일의 물리적 정체를 각도로 확인해 보자.

# %%
moon_deg_per_day = 360.0 / T_SID
earth_deg_per_day = 360.0 / T_YR
earth_moved = earth_deg_per_day * T_SID  # 항성월 동안 지구가 태양 주위로 이동한 각
catch_up_days = earth_moved / moon_deg_per_day

print(f"달의 일주 이동    = {moon_deg_per_day:.4f} deg/day")
print(f"지구의 일주 이동  = {earth_deg_per_day:.4f} deg/day")
print(f"항성월 1회 동안 지구가 이동한 각 = {earth_moved:.4f} deg")
print(f"달이 이 각을 따라잡는 데 걸리는 시간 = {catch_up_days:.4f} 일")
print(f"→ T_sid + 따라잡기 = {T_SID + catch_up_days:.4f} 일  (근사; 엄밀값 {T_syn:.4f})")
# 출력:
# 달의 일주 이동    = 13.1764 deg/day
# 지구의 일주 이동  = 0.9856 deg/day
# 항성월 1회 동안 지구가 이동한 각 = 26.9285 deg
# 달이 이 각을 따라잡는 데 걸리는 시간 = 2.0437 일
# → T_sid + 따라잡기 = 29.3654 일  (근사; 엄밀값 29.5306)
#
# (1차 근사라 0.16일 부족하다. 따라잡는 동안 지구가 또 움직이므로,
#  기하급수 합을 취하면 정확히 회합주기 공식으로 수렴한다.)

# %% [markdown]
# ## 2. 위상 곡선과 도상 요소의 대응
#
# 태양-지구-달 이각을 $\theta(t) = 2\pi t / T_{\text{syn}}$ 로 두면,
# 조명된 원반 비율은
#
# $$f(t) = \frac{1 - \cos\theta(t)}{2}$$
#
# ($\theta=0$ 신월 → $f=0$, $\theta=\pi$ 만월 → $f=1$.)
#
# 리파의 네 요소를 이 곡선 위 국면에 얹으면 각각이 **어느 시점을 지목하는지** 드러난다.

# %%
t = np.linspace(0.0, T_SYN_OBS, 1000)
theta = 2 * np.pi * t / T_SYN_OBS
illum = (1 - np.cos(theta)) / 2

phases = [
    (0.00 * T_SYN_OBS, "신월", "종려 관<br>(신월마다 새 가지)"),
    (0.25 * T_SYN_OBS, "상현", "자라는 송아지<br>(차는 구간)"),
    (0.50 * T_SYN_OBS, "만월", "외뿔이 온전"),
    (0.75 * T_SYN_OBS, "하현", "잘린 뿔<br>(기우는 구간)"),
    (28.0, "월말(28일)", "아래를 향한 두 뿔"),
]

for day, name, icon in phases:
    f = (1 - np.cos(2 * np.pi * day / T_SYN_OBS)) / 2
    print(f"{name:>10s}  t={day:6.3f}일  조명비율={f:.4f}  ← {icon.replace('<br>', ' ')}")
# 출력:
#         신월  t= 0.000일  조명비율=0.0000  ← 종려 관 (신월마다 새 가지)
#         상현  t= 7.383일  조명비율=0.5000  ← 자라는 송아지 (차는 구간)
#         만월  t=14.765일  조명비율=1.0000  ← 외뿔이 온전
#         하현  t=22.148일  조명비율=0.5000  ← 잘린 뿔 (기우는 구간)
#   월말(28일)  t=28.000일  조명비율=0.0263  ← 아래를 향한 두 뿔
#
# 리파가 "달이 28일이 되면 마지막 부분만 빛나고 그 끝이 아래를 향한다"고 쓴 것이
# 조명비율 2.6% — 아주 가느다란 그믐 낫 — 과 정확히 부합한다.

# %% [markdown]
# ## 3. 항성월 '12궁 통과' vs 삭망월 '위상 주기' — 어긋남의 시각화
#
# 달이 12궁 하나를 지나는 데 걸리는 시간은 $T_{sid}/12$이다.
# 항성월 진행률과 삭망월 진행률을 같은 시간축에 그리면,
# **12궁 일주가 끝난 시점에 위상은 아직 한 주기를 못 채운다**는 것이 눈에 보인다.

# %%
days_per_sign = T_SID / 12
print(f"12궁 하나 통과 = {days_per_sign:.4f} 일 ({days_per_sign * 24:.1f} 시간)")
print()
sign_names = ["양", "황소", "쌍둥이", "게", "사자", "처녀", "천칭", "전갈", "궁수", "염소", "물병", "물고기"]
for i, nm in enumerate(sign_names):
    print(f"  {i + 1:2d}. {nm:>4s}자리 진입  t = {i * days_per_sign:6.3f} 일")
print()
print(f"12궁 일주 완료   t = {T_SID:.4f} 일")
print(f"위상 1주기 완료  t = {T_SYN_OBS:.4f} 일")
print(f"어긋남 = {T_SYN_OBS - T_SID:.4f} 일")
frac = T_SID / T_SYN_OBS
print(f"12궁 일주 완료 시점의 위상 진행률 = {frac * 100:.2f} %")
print(f"그 시점 조명비율 = {(1 - np.cos(2 * np.pi * frac)) / 2:.4f}  (신월이 아니라 얇은 그믐달)")
# 출력:
# 12궁 하나 통과 = 2.2768 일 (54.6 시간)
#
#    1.    양자리 진입  t =  0.000 일
#    2.   황소자리 진입  t =  2.277 일
#    3.  쌍둥이자리 진입  t =  4.554 일
#    4.    게자리 진입  t =  6.830 일
#    5.   사자자리 진입  t =  9.107 일
#    6.   처녀자리 진입  t = 11.384 일
#    7.   천칭자리 진입  t = 13.661 일
#    8.   전갈자리 진입  t = 15.938 일
#    9.   궁수자리 진입  t = 18.214 일
#   10.   염소자리 진입  t = 20.491 일
#   11.   물병자리 진입  t = 22.768 일
#   12.  물고기자리 진입  t = 25.045 일
#
# 12궁 일주 완료   t = 27.3217 일
# 위상 1주기 완료  t = 29.5306 일
# 어긋남 = 2.2089 일
# 12궁 일주 완료 시점의 위상 진행률 = 92.52 %
# 그 시점 조명비율 = 0.0542  (신월이 아니라 얇은 그믐달)

# %%
fig = make_subplots(
    rows=2,
    cols=1,
    row_heights=[0.55, 0.45],
    vertical_spacing=0.13,
    subplot_titles=(
        "위상 곡선과 리파의 도상 요소 (삭망월 29.53일)",
        "항성월 12궁 일주 vs 삭망월 위상 주기 — 2.21일 어긋남",
    ),
)

# --- 상단: 위상 곡선 ---
fig.add_trace(
    go.Scatter(
        x=t,
        y=illum,
        mode="lines",
        name="조명 비율 f(t)",
        line=dict(color="#3b6ea5", width=3),
        fill="tozeroy",
        fillcolor="rgba(59,110,165,0.12)",
    ),
    row=1,
    col=1,
)

for day, name, icon in phases:
    f = (1 - np.cos(2 * np.pi * day / T_SYN_OBS)) / 2
    fig.add_trace(
        go.Scatter(
            x=[day],
            y=[f],
            mode="markers",
            marker=dict(size=11, color="#c0392b", line=dict(color="white", width=1.5)),
            name=name,
            showlegend=False,
            hovertemplate=f"{name}<br>t=%{{x:.2f}}일<br>f=%{{y:.3f}}<extra></extra>",
        ),
        row=1,
        col=1,
    )
    fig.add_annotation(
        x=day,
        y=f,
        text=f"<b>{name}</b><br>{icon}",
        showarrow=True,
        arrowhead=2,
        arrowsize=0.8,
        ax=0,
        ay=-52 if f < 0.6 else 46,
        font=dict(size=9.5, color="#7b241c"),
        bgcolor="rgba(255,255,255,0.82)",
        bordercolor="#c0392b",
        borderwidth=0.8,
        row=1,
        col=1,
    )

# --- 하단: 두 진행 트레이스 ---
t2 = np.linspace(0, 33, 800)
prog_sid = t2 / T_SID  # 12궁 일주 진행률
prog_syn = t2 / T_SYN_OBS  # 위상 주기 진행률

fig.add_trace(
    go.Scatter(
        x=t2,
        y=prog_sid,
        mode="lines",
        name="항성월 진행 (12궁 일주)",
        line=dict(color="#1e8449", width=3),
    ),
    row=2,
    col=1,
)
fig.add_trace(
    go.Scatter(
        x=t2,
        y=prog_syn,
        mode="lines",
        name="삭망월 진행 (위상 주기)",
        line=dict(color="#b9770e", width=3, dash="dash"),
    ),
    row=2,
    col=1,
)
fig.add_hline(y=1.0, line=dict(color="#888", width=1, dash="dot"), row=2, col=1)

# 12궁 경계 눈금
for i in range(1, 12):
    fig.add_vline(
        x=i * days_per_sign,
        line=dict(color="rgba(30,132,73,0.22)", width=1),
        row=2,
        col=1,
    )

fig.add_annotation(
    x=T_SID,
    y=1.0,
    text=f"<b>12궁 일주 완료</b><br>{T_SID:.2f}일",
    showarrow=True,
    arrowhead=2,
    ax=-105,
    ay=-20,
    font=dict(size=10, color="#145a32"),
    bgcolor="rgba(255,255,255,0.85)",
    bordercolor="#1e8449",
    borderwidth=0.8,
    row=2,
    col=1,
)
fig.add_annotation(
    x=T_SYN_OBS,
    y=1.0,
    text=f"<b>같은 위상 복귀</b><br>{T_SYN_OBS:.2f}일",
    showarrow=True,
    arrowhead=2,
    ax=54,
    ay=40,
    font=dict(size=10, color="#7e5109"),
    bgcolor="rgba(255,255,255,0.85)",
    bordercolor="#b9770e",
    borderwidth=0.8,
    row=2,
    col=1,
)
fig.add_shape(
    type="rect",
    x0=T_SID,
    x1=T_SYN_OBS,
    y0=0,
    y1=1.0,
    fillcolor="rgba(192,57,43,0.13)",
    line=dict(width=0),
    row=2,
    col=1,
)
fig.add_annotation(
    x=(T_SID + T_SYN_OBS) / 2,
    y=0.42,
    text="<b>2.21일</b><br>리파의 정의가<br>지운 간극",
    showarrow=False,
    font=dict(size=10, color="#7b241c"),
    row=2,
    col=1,
)

fig.update_xaxes(title_text="신월로부터 경과 일수", row=1, col=1, dtick=5)
fig.update_xaxes(title_text="신월로부터 경과 일수", row=2, col=1, dtick=5)
fig.update_yaxes(title_text="조명된 원반 비율", row=1, col=1, range=[-0.16, 1.22])
fig.update_yaxes(title_text="주기 진행률", row=2, col=1, range=[0, 1.22])
fig.update_layout(
    title=dict(
        text="<b>리파 『Iconologia』 '달(月)': 항성월과 삭망월의 혼동</b>",
        x=0.5,
        font=dict(size=16),
    ),
    template="plotly_white",
    width=1000,
    height=800,
    legend=dict(orientation="h", yanchor="bottom", y=-0.11, xanchor="center", x=0.5),
    margin=dict(t=95, b=95),
)

_show(fig)
fig.write_image("expy.png", scale=2)
print("expy.png 저장 완료")
# 출력: expy.png 저장 완료

# %% [markdown]
# ## 4. 역법 비교 — 세 번째 '달'
#
# 리파의 두 주기와 별개로, 우리가 쓰는 **역월**은 태양년을 12로 쪼갠 행정 단위다.
# 12 삭망월과 태양년의 불일치가 태음력·태음태양력 설계 전체를 규정한다.

# %%
lunar_year_12 = 12 * T_SYN_OBS
gap = T_TROP_YR - lunar_year_12

print(f"12 삭망월  = {lunar_year_12:.4f} 일")
print(f"태양년     = {T_TROP_YR:.4f} 일")
print(f"부족분     = {gap:.4f} 일/년")
print()
print("[순태음력: 이슬람 히즈리력]")
for y in (1, 3, 10, 33):
    print(f"  {y:2d}년 후 계절 대비 앞당겨짐: {gap * y:7.2f} 일 ({gap * y / T_TROP_YR:.2f} 태양년)")
print(f"  → 약 {T_TROP_YR / gap:.1f} 태양년마다 계절을 한 바퀴 역행")
print()
print("[태음태양력: 윤달의 필요량]")
print(f"  연간 부족 {gap:.2f}일 → 삭망월 하나({T_SYN_OBS:.2f}일)를 채우려면")
print(f"  {T_SYN_OBS / gap:.3f} 년마다 윤달 1회 (대략 2~3년마다)")
# 출력:
# 12 삭망월  = 354.3671 일
# 태양년     = 365.2422 일
# 부족분     = 10.8751 일/년
#
# [순태음력: 이슬람 히즈리력]
#    1년 후 계절 대비 앞당겨짐:   10.88 일 (0.03 태양년)
#    3년 후 계절 대비 앞당겨짐:   32.63 일 (0.09 태양년)
#   10년 후 계절 대비 앞당겨짐:  108.75 일 (0.30 태양년)
#   33년 후 계절 대비 앞당겨짐:  358.88 일 (0.98 태양년)
#   → 약 33.6 태양년마다 계절을 한 바퀴 역행
#
# [태음태양력: 윤달의 필요량]
#   연간 부족 10.88일 → 삭망월 하나(29.53일)를 채우려면
#   2.715 년마다 윤달 1회 (대략 2~3년마다)

# %% [markdown]
# ## 5. 메톤 주기의 정확도
#
# 기원전 5세기 메톤은 **19 태양년 = 235 삭망월**을 발견했다.
# 19년에 윤달 7개(= 235 − 19×12)를 넣는 방식으로, 동아시아 태음태양력과
# 그리스·유대 역법이 모두 이 주기를 쓴다. 얼마나 정확한가?

# %%
meton_lunar = 235 * T_SYN_OBS
meton_solar = 19 * T_TROP_YR
err = meton_lunar - meton_solar

print(f"235 삭망월 = {meton_lunar:.4f} 일")
print(f" 19 태양년 = {meton_solar:.4f} 일")
print(f"오차       = {err:+.4f} 일 / 19년  ({err * 24:+.2f} 시간)")
print(f"연간 오차  = {err / 19 * 24 * 60:+.2f} 분/년")
print(f"1일 어긋나기까지 = {abs(1 / (err / 19)):.0f} 년")
print()
print(f"윤달 개수: 235 - 19x12 = {235 - 19 * 12} 개 / 19년")
print()
# 대안 주기와 비교
print("주기 후보 비교 (|235/19| 형태의 근사분수):")
for months, years in [(37, 3), (99, 8), (123, 10), (235, 19), (4131, 334)]:
    e = months * T_SYN_OBS - years * T_TROP_YR
    print(f"  {months:5d} 삭망월 = {years:4d} 태양년 : 오차 {e:+8.4f} 일 ({abs(e) / years * 24 * 60:6.2f} 분/년)")
# 출력:
# 235 삭망월 = 6939.6884 일
#  19 태양년 = 6939.6018 일
# 오차       = +0.0866 일 / 19년  (+2.08 시간)
# 연간 오차  = +6.56 분/년
# 1일 어긋나기까지 = 219 년
#
# 윤달 개수: 235 - 19x12 = 7 개 / 19년
#
# 주기 후보 비교 (|235/19| 형태의 근사분수):
#     37 삭망월 =    3 태양년 : 오차  -3.0948 일 (1485.51 분/년)
#     99 삭망월 =    8 태양년 : 오차  +1.5907 일 (286.33 분/년)
#    123 삭망월 =   10 태양년 : 오차 -20.1596 일 (2902.98 분/년)
#    235 삭망월 =   19 태양년 : 오차  +0.0866 일 (  6.56 분/년)
#   4131 삭망월 =  334 태양년 : 오차  -0.0316 일 (  0.14 분/년)
#
# 메톤 주기(19년)는 2시간 오차로, 3년·8년·10년 후보보다 20~300배 정확하다.
# 334년 주기(칼리포스 계열의 더 긴 근사)는 절대오차가 더 작지만
# 사람이 쓰기엔 너무 길다. 19년은 "짧은 주기 + 실용적 정확도"의
# 균형점이라 그리스·유대·동아시아 역법의 공통 표준이 되었다.
# (219년에 1일 어긋나므로 역사적으로 주기적 보정이 필요했다.)

# %% [markdown]
# ## 정리
#
# | 항목 | 값 | 리파의 서술 |
# |---|---|---|
# | 항성월 | 27.3217일 | "12궁을 도는 여정" ← **정의로 제시** |
# | 삭망월 | 29.5306일 | "차고 기움" ← **같은 문장에 병치** |
# | 어긋남 | 2.2089일 | (언급 없음) |
# | 역월(평균) | 30.4369일 | (언급 없음) |
#
# 리파의 도상은 **삭망월의 국면들**(종려=신월, 자라는 송아지=차는 구간,
# 잘린 뿔=기우는 구간, 아래를 향한 두 뿔=28일째)을 정확히 짚는다.
# 그런데 그가 내린 *정의*는 **항성월**의 것이다.
# 상징은 눈에 보이는 위상을 따라갔고, 정의는 책에서 읽은 12궁을 따라간 셈이다.
