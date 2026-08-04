# 작은 힘으로 거대한 무게를 — 리파의 정의를 물리로 읽기

## 0. 출발점: 리파의 문장에서 물리 문제를 뽑아내기

리파는 기계학을

> "**작은 힘(picciola forza)** 으로 **인간의 힘을 넘어서는 거대한 무게** 를 움직이는, 수학(산술·기하)에 근거한 손의 기술"

이라 정의하고, 그 원리를 한마디로 **"기계적 작동은 대부분 원운동에서 유래한다(le operazioni meccaniche... derivano dal moto circolare)"** 로 요약했다. 그리고 지물로 지레(*manuella*)·도르래(*taglia*)·나사(*vite*)·쐐기(*cuneo*)·캡스턴(*argano*)을 들려주었다.

물리학의 언어로 옮기면 질문은 이것이다.

> **작은 힘이 큰 힘을 이기는 것은 공짜인가? 아니라면 무엇을 대가로 내는가?**

답은 **일(work)** 이다. 힘은 줄여 줄 수 있지만 **일은 줄여 주지 못한다.** 이것이 이른바 **기계학의 황금률(the golden rule of mechanics)** 이다.

$$W = F d \quad\Longrightarrow\quad F_{\text{in}}\, d_{\text{in}} \;=\; F_{\text{out}}\, d_{\text{out}}$$

즉 힘을 $n$배 줄이면 이동 거리는 정확히 $n$배 늘어난다. 리파가 말한 "자연의 힘을 이겨낸다"는 것은 **힘(force)** 을 이긴 것이지 **에너지** 를 이긴 것이 아니다.

---

## 1. 지레: *manuella* 와 돌림힘 평형

리파는 *manuella*를 "**그 길이에 비례하여** 원운동으로 무게를 들어 올리는 도구"라 설명하고 아리스토텔레스 『기계학』을 인용한다. 이것이 지레의 법칙이다.

받침점에서 거리 $L_1$인 곳에 힘 $F_1$을, 거리 $L_2$인 곳에 하중 $F_2$를 걸면, 평형 조건은 **돌림힘(토크)의 균형** 이다.

$$\tau = r F \sin\theta, \qquad \vec{\tau} = \vec{r} \times \vec{F}$$

힘이 팔에 수직이면 $\sin\theta = 1$이므로

$$\boxed{F_1 L_1 = F_2 L_2} \qquad\Longrightarrow\qquad \text{MA} \equiv \frac{F_2}{F_1} = \frac{L_1}{L_2}$$

여기서 $\text{MA}$가 **역학적 이득(mechanical advantage)** 이다.

**수치 예.** 길이 $1.5\,\mathrm{m}$인 쇠지레를 하중에서 $L_2 = 0.10\,\mathrm{m}$ 떨어진 곳에 받침을 두고 쓰면 $L_1 = 1.4\,\mathrm{m}$이므로

$$\text{MA} = \frac{1.4}{0.10} = 14$$

사람이 $300\,\mathrm{N}$(약 $30\,\mathrm{kgf}$)으로 누르면 $F_2 = 4200\,\mathrm{N}$, 즉 **약 430 kg** 의 대리석을 든다. 리파의 "인간의 힘을 넘어서는 무게"가 정확히 이것이다.

### 왜 일이 보존되는가 — 원운동이 열쇠

지레는 **하나의 강체** 가 한 축을 중심으로 각 $\theta$만큼 회전하는 것이다. 강체이므로 **양 끝의 회전각 $\theta$는 같다.** 반지름 $L$인 원호의 길이는

$$d = L\theta \quad (\theta \text{는 라디안})$$

이므로 각 끝점의 이동 거리는

$$d_1 = L_1\theta,\qquad d_2 = L_2\theta$$

따라서

$$\frac{d_1}{d_2} = \frac{L_1}{L_2} = \frac{F_2}{F_1} \quad\Longrightarrow\quad F_1 d_1 = F_2 d_2$$

일반적으로 회전에서 한 일은

$$W = \int \tau \, d\theta = \tau\theta$$

이고, 양쪽이 같은 $\theta$를 공유하니 $\tau_1 = \tau_2$가 곧 $W_1 = W_2$다. **"기계적 작동은 원운동에서 유래한다"** 는 리파의 문장은, 물리적으로는 *같은 각변위를 서로 다른 반지름에서 나누어 쓰는 것* 이 모든 단순 기계의 정체라는 뜻이다.

---

## 2. 도르래(*taglia*): 힘을 줄에 나누어 걸기

하중을 떠받치는 줄 가닥이 $n$개이고 마찰과 줄·도르래의 무게를 무시하면, 줄 전체의 장력은 하나의 값 $T$이고

$$nT = W \quad\Longrightarrow\quad F_{\text{in}} = T = \frac{W}{n}, \qquad \text{MA} = n$$

하중을 $h$ 올리려면 $n$가닥이 각각 $h$씩 짧아져야 하므로 손이 당기는 줄의 길이는

$$d_{\text{in}} = nh$$

$$W_{\text{in}} = \frac{W}{n}\cdot nh = Wh = W_{\text{out}} \quad\checkmark$$

$n=6$이면 힘은 $1/6$, 당길 줄은 6배. 리파가 *taglia*를 "수평으로도 수직으로도 아무리 큰 무게를 끌고 올린다"고 한 이유다.

---

## 3. 캡스턴(*argano*): 반지름 비가 곧 이득

리파가 "중심 자리에 놓인 원운동으로 **초자연적인 무게** 를 끈다"고 한 *argano*는 반지름 $r$인 드럼에 반지름 $R$인 지렛대(손잡이)를 꽂은 장치다. 손잡이를 한 바퀴 돌리면

- 손이 지나간 거리: $d_{\text{in}} = 2\pi R$
- 감긴 줄의 길이: $d_{\text{out}} = 2\pi r$

$$\text{MA} = \frac{d_{\text{in}}}{d_{\text{out}}} = \frac{R}{r}$$

$R = 2\,\mathrm{m}$, $r = 0.15\,\mathrm{m}$면 $\text{MA} \approx 13$. 여기에 도르래 $n=4$를 직렬로 붙이면 이득이 **곱** 으로 쌓인다.

$$\text{MA}_{\text{total}} = \text{MA}_1 \times \text{MA}_2 \times \cdots \approx 13 \times 4 = 52$$

$400\,\mathrm{N}$의 사람 넷($1600\,\mathrm{N}$)이 $8.3\times10^4\,\mathrm{N}$, 약 **8.5톤** 을 끈다. 르네상스 건축 현장의 "경이로운 일"은 이런 곱셈의 결과였다.

---

## 4. 경사면 → 쐐기(*cuneo*)와 나사(*vite*)

### 경사면

각 $\theta$인 마찰 없는 경사면에서 질량 $m$을 밀어 올릴 때 필요한 힘과 이동 거리는

$$F = mg\sin\theta, \qquad d = \frac{h}{\sin\theta}$$

$$W = Fd = mg\sin\theta \cdot \frac{h}{\sin\theta} = mgh$$

높이 $h$만 같으면 경사가 완만하든 급하든 **일은 동일** 하다. $\text{MA} = 1/\sin\theta$.

### 쐐기

쐐기는 움직이는 경사면이다. 길이 $L$, 뒷면 두께 $t$인 쐐기를 $L$만큼 박아 넣으면 양쪽 면은 각각 $t/2$씩 벌어진다.

$$\text{MA} \approx \frac{L}{t} = \frac{1}{\tan(\theta/2)}\ \text{규모}$$

$L = 20\,\mathrm{cm}$, $t = 2\,\mathrm{cm}$면 $\text{MA} \approx 10$. 리파의 "타격을 받으면 어떤 단단한 것도 쪼갠다"가 이 값이다. (실제 석재 쪼개기에서는 정적 힘의 이득에 더해 망치의 운동에너지 $\frac{1}{2}mv^2$가 아주 짧은 시간에 전달되어 순간 힘 $F \approx \Delta p/\Delta t$가 커지는 효과가 겹친다.)

### 나사

나사는 실린더에 감긴 경사면이다. 피치(한 바퀴당 전진 거리)를 $p$, 손잡이(또는 렌치) 반지름을 $R$라 하면 한 바퀴에

$$d_{\text{in}} = 2\pi R, \qquad d_{\text{out}} = p$$

$$\boxed{\text{MA}_{\text{ideal}} = \frac{2\pi R}{p}}$$

$R = 0.3\,\mathrm{m}$, $p = 5\,\mathrm{mm}$이면 $\text{MA} = 2\pi(0.3)/0.005 \approx 377$. 리파가 나사를 "위 도구들보다 **더 쉽게**(*con maggior facilità*) 무거운 기계를 들어 올린다"고 한 판단은 정확하다 — 단순 기계 중 이상적 이득이 가장 크다.

---

## 5. 대가는 힘만이 아니다 — 효율과 마찰

실제 기계에서 넣은 일의 일부는 마찰로 열이 된다.

$$\eta = \frac{W_{\text{out}}}{W_{\text{in}}} = \frac{F_{\text{out}} d_{\text{out}}}{F_{\text{in}} d_{\text{in}}} \le 1$$

$$\text{MA}_{\text{real}} = \eta \cdot \text{MA}_{\text{ideal}}$$

흥미로운 점은 **나사의 효율이 매우 낮다는 사실($\eta$가 흔히 0.2~0.4)이 오히려 장점** 이라는 것이다. 효율이 낮으면 하중이 스스로 나사를 되돌리지 못한다(**자동 잠김, self-locking**). 대략적인 조건은

$$\tan\alpha < \mu_s, \qquad \tan\alpha = \frac{p}{2\pi r}$$

여기서 $\alpha$는 나사산의 리드각, $\mu_s$는 정지마찰계수다. 그래서 잭으로 든 무게가 손을 떼도 내려오지 않는다. 리파가 나사를 "들어 올리는 데도, **조이는(stringere)** 데도 쓴다"고 병기한 이유가 여기 있다.

---

## 6. 힘·속도·일률로 다시 쓰기

양변을 시간으로 미분하면 같은 법칙이 **일률(power)** 형태로 나온다. $W = Fd$에서

$$P = \frac{dW}{dt} = F\frac{dd}{dt} = Fv$$

이상적 기계는 일률을 그대로 전달하므로

$$F_{\text{in}} v_{\text{in}} = F_{\text{out}} v_{\text{out}}$$

즉 **힘 × 속도가 보존량** 이다. 힘을 100배 얻으면 속도는 100분의 1. 이 형태는 일반화된 증명(가상일의 원리)에도 그대로 쓰인다: 구속 조건이 일을 하지 않는 기계에서 미소 변위 $\delta$에 대해

$$\sum_i \vec{F}_i \cdot \delta \vec{r}_i = 0$$

지레·도르래·나사의 개별 공식은 모두 이 한 줄의 특수한 경우다.

---

## 7. 아르키메데스의 지구 — "왜 원리상 가능하지만 실제로는 불가능한가"

> "발 디딜 곳을 주면 지구를 움직여 보이겠다." — 아르키메데스

리파의 "인간의 힘을 넘어서는 무게"의 극한 버전이다. $F_1 L_1 = F_2 L_2$에는 **상한이 없으므로 원리상 가능** 하다. 문제는 대가로 지불해야 할 **거리** 다.

지구의 무게(질량 $M = 6.0\times10^{24}\,\mathrm{kg}$, $g = 9.8\,\mathrm{m/s^2}$)를

$$W_{\text{Earth}} = Mg \approx 5.9\times10^{25}\,\mathrm{N}$$

사람이 낼 수 있는 힘을 $F_1 = 700\,\mathrm{N}$이라 하면 필요한 역학적 이득은

$$\text{MA} = \frac{5.9\times10^{25}}{700} \approx 8.4\times10^{22}$$

**(1) 지레의 길이.** 하중측 팔을 $L_2 = 1\,\mathrm{m}$로 두면

$$L_1 = 8.4\times10^{22}\,\mathrm{m} \approx 8.9\times10^{6}\ \text{광년}$$

(1 광년 $= 9.46\times10^{15}\,\mathrm{m}$) — 우리 은하 지름의 약 90배인 막대가 필요하다.

**(2) 손이 움직여야 하는 거리.** 지구를 고작 $1\,\mathrm{cm}$ 들어 올리려 해도 황금률에 따라

$$d_1 = \text{MA} \times d_2 = 8.4\times10^{22} \times 0.01\,\mathrm{m} = 8.4\times10^{20}\,\mathrm{m} \approx 8.9\times10^{4}\ \text{광년}$$

즉 **약 9만 광년** — 우리 은하를 한 번 가로지르는 거리다.

**(3) 걸리는 시간.** $v = 1\,\mathrm{m/s}$로 꾸준히 밀어도

$$t = \frac{8.4\times10^{20}}{1} \,\mathrm{s} \approx 2.7\times10^{13}\ \text{년}$$

우주의 나이($1.38\times10^{10}$년)의 약 **2000배**. 게다가 신호가 막대를 따라 전달되는 속도는 광속을 넘을 수 없고, 그 길이의 강체 막대는 자기 무게로 붕괴한다.

**결론:** 아르키메데스의 호언은 $F_1 L_1 = F_2 L_2$에 힘의 상한이 없다는 점에서 **수학적으로 참** 이지만, $W = Fd$가 보존되기 때문에 **거리·시간이라는 청구서** 가 그대로 남는다. 리파가 기계학을 "자연의 힘을 이긴다"고 표현한 것은 그래서 절반만 맞다. 기계는 **힘을 재분배** 할 뿐, 자연의 보존법칙을 벗어나지 못한다.

---

## 8. 한 장 요약

| 기계 (리파의 지물) | 이상적 이득 $\text{MA}$ | 대가로 늘어나는 거리 |
|---|---|---|
| 지레 *manuella* | $L_1/L_2$ | $d_1 = (L_1/L_2)\,d_2$ |
| 도르래 *taglia* | 줄 가닥 수 $n$ | $nh$ |
| 캡스턴 *argano* | $R/r$ | $2\pi R$ 당 $2\pi r$ |
| 쐐기 *cuneo* | $L/t$ | 박는 깊이 $L$ 당 벌어짐 $t$ |
| 나사 *vite* | $2\pi R/p$ | 한 바퀴 $2\pi R$ 당 전진 $p$ |
| 경사면 | $1/\sin\theta$ | $h/\sin\theta$ |

**모두 관통하는 하나의 식**

$$F_{\text{in}} d_{\text{in}} = F_{\text{out}} d_{\text{out}} \quad\Longleftrightarrow\quad \tau_{\text{in}}\theta = \tau_{\text{out}}\theta \quad\Longleftrightarrow\quad F_{\text{in}}v_{\text{in}} = F_{\text{out}}v_{\text{out}}$$

리파가 머리 위에 **원** 을 그려 넣은 것은, 400년 전의 언어로 이 등식의 공통 변수 $\theta$를 가리킨 셈이다.
