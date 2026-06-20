---
Created: 2026-03-10T04:59
Reviewed: Doing
---
## Forward процесс диффузии

### Определение

Пусть $\mathbf{x}_0 = \mathbf{x} \sim p_{\text{data}}(\mathbf{x})$ — сэмпл из распределения данных. Определим марковскую цепь, которая постепенно добавляет гауссовский шум к данным. На каждом шаге $t$ сэмпл $\mathbf{x}_t$ получается из предыдущего $\mathbf{x}_{t-1}$ следующим образом:

$$\mathbf{x}_t = \sqrt{1 - \beta_t} \cdot \mathbf{x}_{t-1} + \sqrt{\beta_t} \cdot \boldsymbol{\epsilon}_t, \quad \boldsymbol{\epsilon}_t \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$$

где $\beta_t \ll 1$ — расписание шума (noise schedule), контролирующее интенсивность добавляемого шума на каждом шаге. Эквивалентно, переходное распределение записывается как:

$$q(\mathbf{x}_t | \mathbf{x}_{t-1}) = \mathcal{N}\left(\sqrt{1 - \beta_t} \cdot \mathbf{x}_{t-1},\ \beta_t \mathbf{I}\right)$$

Обратим внимание на структуру этого перехода. Коэффициент $\sqrt{1 - \beta_t}$ перед $\mathbf{x}_{t-1}$ слегка сжимает сигнал к нулю, а слагаемое $\sqrt{\beta_t} \cdot \boldsymbol{\epsilon}_t$ добавляет случайный шум. Таким образом, на каждом шаге мы немного “забываем” информацию о данных и заменяем её шумом.

### Связь с forward процесса с динамикой Ланжевена

Эта марковская цепь не случайна — она является частным случаем динамики Ланжевена. Вспомним формулу из раздела NCSN:

$$\mathbf{x}_{l+1} = \mathbf{x}_l + \frac{\eta}{2} \nabla_{\mathbf{x}_l} \log p(\mathbf{x}_l) + \sqrt{\eta} \cdot \boldsymbol{\epsilon}_l, \quad \boldsymbol{\epsilon}_l \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$$

Теперь покажем, что формула прямого диффузионного процесса сводится к динамике Ланжевена со score-функцией стандартного нормального распределения. Для этого нам понадобится разложить $\sqrt{1 - \beta_t}$ при малых $\beta_t$.

- **Разложение Тейлора**
    
    Вспомним обобщённый биномиальный ряд: для функции $f(x) = (1 + x)^a$ при $|x| \ll 1$ разложение Тейлора в окрестности $x = 0$ имеет вид:
    
    $$(1 + x)^a = 1 + ax + \frac{a(a-1)}{2!}x^2 + \ldots \approx 1 + ax$$
    
    где мы оставляем только линейный член, отбрасывая $O(x^2)$. В нашем случае $a = \frac{1}{2}$ и $x = -\beta_t$:
    

$$\sqrt{1 - \beta_t} = (1 + (-\beta_t))^{1/2} \approx 1 + \frac{1}{2}(-\beta_t) = 1 - \frac{\beta_t}{2}$$

Это приближение корректно, поскольку $\beta_t \ll 1$ по построению. Подставляем:

$$\mathbf{x}_t = \sqrt{1 - \beta_t} \cdot \mathbf{x}_{t-1} + \sqrt{\beta_t} \cdot \boldsymbol{\epsilon}_t \approx \left(1 - \frac{\beta_t}{2}\right) \mathbf{x}_{t-1} + \sqrt{\beta_t} \cdot \boldsymbol{\epsilon}_t$$

Перегруппируем:

$$\mathbf{x}_t = \mathbf{x}_{t-1} + \frac{\beta_t}{2}(-\mathbf{x}_{t-1}) + \sqrt{\beta_t} \cdot \boldsymbol{\epsilon}_t$$

Сравнивая с формулой Ланжевена, получаем:

- $\eta = \beta_t$ — размер шага

- $\nabla_{\mathbf{x}_{t-1}} \log p(\mathbf{x}_{t-1}) = -\mathbf{x}_{t-1}$

Но $-\mathbf{x}$ — это в точности score-функция стандартного нормального распределения! Действительно:

$$\nabla_{\mathbf{x}} \log \mathcal{N}(\mathbf{x} \mid \mathbf{0}, \mathbf{I}) = \nabla_{\mathbf{x}} \left( -\frac{\|\mathbf{x}\|^2}{2} + \text{const} \right) = -\mathbf{x}$$

Таким образом, прямой диффузионный процесс — это динамика Ланжевена, которая сэмплирует из $\mathcal{N}(\mathbf{0}, \mathbf{I})$. Это сразу даёт нам интуицию: **стационарное распределение этой цепи — стандартное нормальное**, потому что динамика Ланжевена сходится к распределению, чей score используется в качестве дрейфа.

### Прямой переход от $\mathbf{x}_0$ к $\mathbf{x}_t$

Марковская цепь позволяет получить $\mathbf{x}_t$ последовательным применением $t$ шагов. Однако можно показать, что существует замкнутая формула для перехода сразу от $\mathbf{x}_0$ к $\mathbf{x}_t$ за один шаг. Введем следующие обозначения:

$$\begin{aligned}  
\alpha_t = 1 - \beta_t \\  
\bar{\alpha}_t = \prod_{s=1}^{t} \alpha_s = \prod_{s=1}^{t}(1 - \beta_s)  
\end{aligned}$$

Тогда сэмпл на шаге $t$ можно получить напрямую из $\mathbf{x}_0$ следующим образом:

$$\begin{aligned}  
q(\mathbf{x}_t | \mathbf{x}_0) = \mathcal{N}\left(\sqrt{\bar{\alpha}_t} \cdot \mathbf{x}_0,\ (1 - \bar{\alpha}_t) \mathbf{I}\right) \\  
или  
\\  
\mathbf{x}_t = \sqrt{\bar{\alpha}_t} \cdot \mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t} \cdot \boldsymbol{\epsilon}, \quad \boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})  
\end{aligned}$$

- **Доказательство**
    
    Проведём индукцию, раскручивая рекурсию. Начнём с одного шага:
    
    $$\mathbf{x}_t = \sqrt{\alpha_t} \cdot \mathbf{x}_{t-1} + \sqrt{1 - \alpha_t} \cdot \boldsymbol{\epsilon}_t$$
    
    Подставим $\mathbf{x}_{t-1} = \sqrt{\alpha_{t-1}} \cdot \mathbf{x}_{t-2} + \sqrt{1 - \alpha_{t-1}} \cdot \boldsymbol{\epsilon}_{t-1}$:
    
    $$\mathbf{x}_t = \sqrt{\alpha_t} \left( \sqrt{\alpha_{t-1}} \cdot \mathbf{x}_{t-2} + \sqrt{1 - \alpha_{t-1}} \cdot \boldsymbol{\epsilon}_{t-1} \right) + \sqrt{1 - \alpha_t} \cdot \boldsymbol{\epsilon}_t$$
    
    $$= \sqrt{\alpha_t \alpha_{t-1}} \cdot \mathbf{x}_{t-2} + \underbrace{\sqrt{\alpha_t(1 - \alpha_{t-1})} \cdot \boldsymbol{\epsilon}_{t-1} + \sqrt{1 - \alpha_t} \cdot \boldsymbol{\epsilon}_t}_{\text{сумма двух независимых гауссиан}}$$
    
    Сумма двух независимых нормальных случайных величин $\mathcal{N}(0, \sigma_1^2 \mathbf{I})$ и $\mathcal{N}(0, \sigma_2^2 \mathbf{I})$ даёт $\mathcal{N}(0, (\sigma_1^2 + \sigma_2^2)\mathbf{I})$. Суммарная дисперсия:
    
    $$\alpha_t(1 - \alpha_{t-1}) + (1 - \alpha_t) = \alpha_t - \alpha_t \alpha_{t-1} + 1 - \alpha_t = 1 - \alpha_t \alpha_{t-1}$$
    
    Значит:
    
    $$\mathbf{x}_t = \sqrt{\alpha_t \alpha_{t-1}} \cdot \mathbf{x}_{t-2} + \sqrt{1 - \alpha_t \alpha_{t-1}} \cdot \boldsymbol{\epsilon}', \quad \boldsymbol{\epsilon}' \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$$
    
    Продолжая подстановку до $\mathbf{x}_0$, получаем:
    
    $$\mathbf{x}_t = \sqrt{\bar{\alpha}_t} \cdot \mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t} \cdot \boldsymbol{\epsilon}, \quad \boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$$
    
    Что и требовалось доказать. $\blacksquare$
    

### Итого

Прямой диффузионный процесс можно подытожить следующим образом:

1. $\mathbf{x}_0 = \mathbf{x} \sim p_{\text{data}}(\mathbf{x})$

1. $\mathbf{x}_t = \sqrt{1 - \beta_t} \cdot \mathbf{x}_{t-1} + \sqrt{\beta_t} \cdot \boldsymbol{\epsilon}, \quad \boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I}), \quad t \geq 1$

1. После $T \gg 1$ шагов: $\mathbf{x}_T \sim p_\infty(\mathbf{x}) = \mathcal{N}(\mathbf{0}, \mathbf{I})$

Диффузия описывает миграцию частиц из областей высокой плотности в области низкой плотности. Если мы сумеем обратить этот процесс, то сможем генерировать сэмплы из $p_{\text{data}}(\mathbf{x})$, стартуя из шума $p_\infty(\mathbf{x}) = \mathcal{N}(\mathbf{0}, \mathbf{I})$.

## Denoising Score Matching for Diffusion

### Аналогия с NCSN

В разделе NCSN мы обучали score-функцию для нескольких уровней шума, используя процесс зашумления:

$$q(\mathbf{x}_\sigma \mid \mathbf{x}_0) = \mathcal{N}(\mathbf{x}_0,\ \sigma^2 \mathbf{I})$$

с граничными условиями $q(\mathbf{x}_1) \approx p_{\text{data}}(\mathbf{x})$ при малом $\sigma_1$ и $q(\mathbf{x}_T) \approx \mathcal{N}(\mathbf{0},\ \sigma_T^2 \mathbf{I})$ при большом $\sigma_T$. Score условного распределения имел вид:

$$\nabla_{\mathbf{x}_\sigma} \log q(\mathbf{x}_\sigma \mid \mathbf{x}) = -\frac{\mathbf{x}_\sigma - \mathbf{x}}{\sigma^2} = -\boldsymbol{\epsilon}/\sigma$$

Теперь заметим, что прямой диффузионный процесс задаёт очень похожую структуру зашумления, но с другой параметризацией. Из замкнутой формулы мы знаем:

$$q(\mathbf{x}_t \mid \mathbf{x}_0) = \mathcal{N}\left(\sqrt{\bar{\alpha}_t} \cdot \mathbf{x}_0,\ (1 - \bar{\alpha}_t) \mathbf{I}\right)$$

с граничными условиями $q(\mathbf{x}_1) \approx p_{\text{data}}(\mathbf{x})$ при $\bar{\alpha}_1 \approx 1$ и $q(\mathbf{x}_T) \approx \mathcal{N}(\mathbf{0}, \mathbf{I})$ при $\bar{\alpha}_T \approx 0$.

Отличие от NCSN в том, что здесь среднее сдвинуто: вместо $\mathbf{x}_0$ стоит $\sqrt{\bar{\alpha}_t} \cdot \mathbf{x}_0$. Однако это не меняет сути — мы по-прежнему зашумляем данные гауссовским шумом и знаем условное распределение в замкнутом виде.

### Score условного распределения

Вычислим score условного распределения $q(\mathbf{x}_t \mid \mathbf{x}_0)$ для диффузионного процесса. Логарифм гауссовой плотности:

$$\log q(\mathbf{x}_t \mid \mathbf{x}_0) = -\frac{\|\mathbf{x}_t - \sqrt{\bar{\alpha}_t} \cdot \mathbf{x}_0\|^2}{2(1 - \bar{\alpha}_t)} + \text{const}$$

Берём градиент по $\mathbf{x}_t$:

$$\nabla_{\mathbf{x}_t} \log q(\mathbf{x}_t \mid \mathbf{x}_0) = -\frac{\mathbf{x}_t - \sqrt{\bar{\alpha}_t} \cdot \mathbf{x}_0}{1 - \bar{\alpha}_t}$$

Вспомним, что $\mathbf{x}_t = \sqrt{\bar{\alpha}_t} \cdot \mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t} \cdot \boldsymbol{\epsilon}$, где $\boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$. Подставим:

$$\nabla_{\mathbf{x}_t} \log q(\mathbf{x}_t \mid \mathbf{x}_0) = -\frac{\sqrt{1 - \bar{\alpha}_t} \cdot \boldsymbol{\epsilon}}{1 - \bar{\alpha}_t} = -\frac{\boldsymbol{\epsilon}}{\sqrt{1 - \bar{\alpha}_t}}$$

Сравним с NCSN, где score условного распределения был $-\boldsymbol{\epsilon}/\sigma$. Видим полную аналогию: роль $\sigma$ здесь играет $\sqrt{1 - \bar{\alpha}_t}$.

### Применение теоремы DSM

В разделе Energy-Based models мы доказали теорему Denoising Score Matching:

$$\mathbb{E}_{q(\mathbf{x}_t)} \left\| \mathbf{s}_{\theta,t}(\mathbf{x}_t) - \nabla_{\mathbf{x}_t} \log q(\mathbf{x}_t) \right\|_2^2 = \mathbb{E}_{p_{\text{data}}(\mathbf{x}_0)} \mathbb{E}_{q(\mathbf{x}_t \mid \mathbf{x}_0)} \left\| \mathbf{s}_{\theta,t}(\mathbf{x}_t) - \nabla_{\mathbf{x}_t} \log q(\mathbf{x}_t \mid \mathbf{x}_0) \right\|_2^2 + \text{const}(\theta)$$

Эта теорема универсальна — она справедлива для любого условного распределения $q(\mathbf{x}_t \mid \mathbf{x}_0)$, в том числе и для диффузионного. Ключевой выигрыш остаётся тем же: неизвестный score маргинала $\nabla_{\mathbf{x}_t} \log q(\mathbf{x}_t)$ заменяется на известный score условного распределения $\nabla_{\mathbf{x}_t} \log q(\mathbf{x}_t \mid \mathbf{x}_0)$.

Подставляя вычисленный выше score и переписывая ожидание по $q(\mathbf{x}_t \mid \mathbf{x}_0)$ как ожидание по $\boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$, получаем задачу оптимизации:

$$\mathbb{E}_{p_{\text{data}}(\mathbf{x}_0)} \mathbb{E}_{\boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})} \left\| \mathbf{s}_{\theta,t}\!\left(\sqrt{\bar{\alpha}_t} \cdot \mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t} \cdot \boldsymbol{\epsilon}\right) + \frac{\boldsymbol{\epsilon}}{\sqrt{1 - \bar{\alpha}_t}} \right\|_2^2 \rightarrow \min_\theta$$

Таким образом, подход NCSN с annealed динамикой Ланжевена напрямую переносится на диффузионные модели: вместо дискретного набора уровней шума $\{\sigma_i\}$ мы используем расписание $\{\beta_t\}$, а роль $\sigma_i$ играет $\sqrt{1 - \bar{\alpha}_t}$.

### Визуальное сравнение: Forward Diffusion vs NCSN / DSM

Анимация ниже наглядно демонстрирует ключевое различие между двумя процессами зашумления. Слева — forward diffusion (DDPM): облако точек одновременно мигрирует к началу координат и размывается. Справа — NCSN/DSM: облако остаётся на месте, увеличивается только дисперсия. В обоих случаях используются одни и те же исходные данные $\mathbf{x}_0$ и один и тот же шум $\boldsymbol{\epsilon}$ — отличается только преобразование.

![[images/ddpm/97d586ea-075a-4030-ab13-998664bd6c88.gif]]

## Reverse Gaussian Diffusion Process

### Цель: обращение диффузии

Мы показали, что прямой диффузионный процесс превращает любое распределение данных $p_{\text{data}}(\mathbf{x})$ в стандартное нормальное $\mathcal{N}(\mathbf{0}, \mathbf{I})$. Если мы сумеем обратить этот процесс — то есть найти переходное распределение $q(\mathbf{x}_{t-1} \mid \mathbf{x}_t)$ — мы сможем генерировать сэмплы из $p_{\text{data}}(\mathbf{x})$, стартуя из чистого шума.

По формуле Байеса:

$$q(\mathbf{x}_{t-1} \mid \mathbf{x}_t) = \frac{q(\mathbf{x}_t \mid \mathbf{x}_{t-1}) \cdot q(\mathbf{x}_{t-1})}{q(\mathbf{x}_t)}$$

Однако маргинальные распределения $q(\mathbf{x}_{t-1})$ и $q(\mathbf{x}_t)$ неизвестны в замкнутом виде — они зависят от распределения данных:

$$q(\mathbf{x}_t) = \int q(\mathbf{x}_t \mid \mathbf{x}_0) \, p_{\text{data}}(\mathbf{x}_0) \, d\mathbf{x}_0$$

Этот интеграл по всему пространству данных аналитически неразрешим — мы не знаем $p_{\text{data}}(\mathbf{x}_0)$ в замкнутом виде. Таким образом, точное обратное распределение $q(\mathbf{x}_{t-1} \mid \mathbf{x}_t)$ нам недоступно.

### Теорема Феллера

Несмотря на то что точное обратное распределение неизвестно, важный теоретический результат гарантирует, что оно имеет простую форму.

**Теорема (Feller, 1949).** Если шаг $\beta_t$ достаточно мал, то обратное переходное распределение $q(\mathbf{x}_{t-1} \mid \mathbf{x}_t)$ является гауссовским.

- **Интуиция**
    
    По формуле Байеса обратный переход раскладывается как
    
    $$q(\mathbf{x}_{t-1} \mid \mathbf{x}_t) \;\propto\; \underbrace{q(\mathbf{x}_t \mid \mathbf{x}_{t-1})}_{\text{известная гауссиана}} \cdot \underbrace{q(\mathbf{x}_{t-1})}_{\text{сложное априори}}$$
    
    Знаменатель $q(\mathbf{x}_t)$ — нормировочная константа и на форму не влияет. Значит, всё решает числитель: произведение простой гауссианы на вообще говоря мультимодальное распределение данных. Вопрос: почему это произведение всё равно оказывается гауссовским?
    
    **1. Узкое окно.** Рассмотрим первый множитель $q(\mathbf{x}_t \mid \mathbf{x}_{t-1})$ как функцию от $\mathbf{x}_{t-1}$ при фиксированном $\mathbf{x}_t$. Это гауссиана с центром около $\mathbf{x}_t / \sqrt{\alpha_t}$ _и шириной $\sim \sqrt{\beta_t}$. При малом $\beta_t$ этот пик очень узкий: он как «прожектор», обнуляющий произведение везде, кроме крошечной окрестности. Поэтому нам не важно, как $q(\mathbf{x}_{t-1})$_ выглядит глобально — важно только её поведение в окне шириной $\sqrt{\beta_t}$.
    
    **2. Любая гладкая функция локально — парабола.** Разложим $\log q(\mathbf{x}_{t-1})$ по Тейлору вокруг центра окна $\mathbf{x}^{*}$:
    
    $$\log q(\mathbf{x}_{t-1}) \approx \log q(\mathbf{x}^{*}) + (\mathbf{x}_{t-1} - \mathbf{x}^{*})^{\top} \nabla \log q(\mathbf{x}^{*}) + \tfrac{1}{2}(\mathbf{x}_{t-1} - \mathbf{x}^{*})^{\top} \mathbf{H}\, (\mathbf{x}_{t-1} - \mathbf{x}^{*}) + \ldots$$
    
    В окне ширины $\sqrt{\beta_t}$ смещение $\|\mathbf{x}_{t-1} - \mathbf{x}^{*}\| \sim \sqrt{\beta_t}$, и члены разложения масштабируются как
    
    $$\text{квадратичный}: \mathcal{O}(\beta_t), \qquad \text{кубический}: \mathcal{O}(\beta_t^{3/2}), \qquad \text{и так далее.}$$
    
    При $\beta_t \to 0$ кубический и высшие члены исчезают **быстрее** квадратичного, и их можно отбросить. В узком окне $\log q(\mathbf{x}_{t-1})$ хорошо приближается квадратичной функцией.
    
    **3. Собираем.** Подставляем в логарифм постериора:
    
    $$\log q(\mathbf{x}_{t-1} \mid \mathbf{x}_t) = \underbrace{\log q(\mathbf{x}_t \mid \mathbf{x}_{t-1})}_{\text{квадратично по } \mathbf{x}_{t-1}} \;+\; \underbrace{\log q(\mathbf{x}_{t-1})}_{\approx\, \text{квадратично}} \;+\; \text{const}$$
    
    Сумма двух квадратичных форм — квадратичная форма; экспонента от неё — гауссиана. Значит, $q(\mathbf{x}_{t-1} \mid \mathbf{x}_t)$ приближённо гауссовское. Это ровно аргумент **приближения Лапласа**: когда один из множителей — узкая гауссиана, второй можно «заморозить» на уровне квадратичного приближения, и произведение остаётся гауссовым.
    
    ![[images/ddpm/image.png|image.png]]
    

### Аппроксимация обратного процесса

Теорема Феллера даёт нам право аппроксимировать обратное распределение нормальным:

$$q(\mathbf{x}_{t-1} \mid \mathbf{x}_t) \approx p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t) = \mathcal{N}\!\left(\boldsymbol{\mu}_{\theta,t}(\mathbf{x}_t),\; \sigma^2_{\theta,t}(\mathbf{x}_t) \cdot \mathbf{I}\right)$$

где $\boldsymbol{\mu}_{\theta,t}$ и $\sigma^2_{\theta,t}$ — обучаемые функции, параметризованные вектором $\theta$. Таким образом, задача сводится к обучению этих функций.

Теперь мы можем записать прямой и обратный процессы симметрично:

||Прямой процесс|Обратный процесс|
|---|---|---|
|Инициализация|$\mathbf{x}_0 \sim p_{\text{data}}(\mathbf{x})$|$\mathbf{x}_T \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$|
|Переход|$\mathbf{x}_t = \sqrt{1 - \beta_t} \cdot \mathbf{x}_{t-1} + \sqrt{\beta_t} \cdot \boldsymbol{\epsilon}$|$\mathbf{x}_{t-1} = \boldsymbol{\mu}_{\theta,t}(\mathbf{x}_t) + \sigma_{\theta,t}(\mathbf{x}_t) \cdot \boldsymbol{\epsilon}$|
|Результат|$\mathbf{x}_T \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$|$\mathbf{x}_0 \sim p_{\text{data}}(\mathbf{x})$|

Важно отметить асимметрию: прямой процесс **не содержит обучаемых параметров** — расписание $\{\beta_t\}$ задано заранее. Все параметры сосредоточены в обратном процессе.

### Условное обратное распределение

Мы показали, что безусловное обратное распределение $q(\mathbf{x}_{t-1} \mid \mathbf{x}_t)$ неразрешимо аналитически — для его вычисления нужны неизвестные маргиналы $q(\mathbf{x}_{t-1})$ и $q(\mathbf{x}_t)$. Однако если мы дополнительно зафиксируем начальную точку $\mathbf{x}_0$, ситуация кардинально меняется. Запишем условное обратное распределение по формуле Байеса:

$$q(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{x}_0) = \frac{q(\mathbf{x}_t \mid \mathbf{x}_{t-1}, \mathbf{x}_0) \cdot q(\mathbf{x}_{t-1} \mid \mathbf{x}_0)}{q(\mathbf{x}_t \mid \mathbf{x}_0)}$$

Ключевое наблюдение: все три распределения в этой дроби нам **известны в замкнутом виде**. Разберём каждое:

- $q(\mathbf{x}_t \mid \mathbf{x}_{t-1}, \mathbf{x}_0) = q(\mathbf{x}_t \mid \mathbf{x}_{t-1})$ — следствие марковского свойства: зная $\mathbf{x}_{t-1}$, информация о $\mathbf{x}_0$ не добавляет ничего нового для предсказания $\mathbf{x}_t$. Это обычный прямой переход:

$$q(\mathbf{x}_t \mid \mathbf{x}_{t-1}) = \mathcal{N}\!\left(\sqrt{\alpha_t} \cdot \mathbf{x}_{t-1},\; \beta_t \mathbf{I}\right)$$

- $q(\mathbf{x}_{t-1} \mid \mathbf{x}_0)$ — прямой переход от $\mathbf{x}_0$ к $\mathbf{x}_{t-1}$, выведенный ранее:

$$q(\mathbf{x}_{t-1} \mid \mathbf{x}_0) = \mathcal{N}\!\left(\sqrt{\bar{\alpha}_{t-1}} \cdot \mathbf{x}_0,\; (1 - \bar{\alpha}_{t-1}) \mathbf{I}\right)$$

- $q(\mathbf{x}_t \mid \mathbf{x}_0)$ — аналогично:

$$q(\mathbf{x}_t \mid \mathbf{x}_0) = \mathcal{N}\!\left(\sqrt{\bar{\alpha}_t} \cdot \mathbf{x}_0,\; (1 - \bar{\alpha}_t) \mathbf{I}\right)$$

Итого, задача сводится к произведению и делению трёх гауссиан — результат гарантированно будет гауссианой. Вывод параметров мы опустим, нужно просто перемножить пару гауссиан, сразу перейдем к результату:

**Дисперсия:**

$$\tilde{\beta}_t = \frac{(1 - \alpha_t)(1 - \bar{\alpha}_{t-1})}{1 - \bar{\alpha}_t}$$

Обратим внимание: дисперсия $\tilde{\beta}_t$ зависит только от расписания шума $\{\beta_t\}$ и **не зависит** от $\mathbf{x}_t$ или $\mathbf{x}_0$. Это константа, полностью определённая на этапе задания гиперпараметров модели.

**Среднее:**

$$\tilde{\boldsymbol{\mu}}_t(\mathbf{x}_t, \mathbf{x}_0) = \frac{\sqrt{\alpha_t}(1 - \bar{\alpha}_{t-1})}{1 - \bar{\alpha}_t} \cdot \mathbf{x}_t + \frac{\sqrt{\bar{\alpha}_{t-1}}(1 - \alpha_t)}{1 - \bar{\alpha}_t} \cdot \mathbf{x}_0$$

Среднее — взвешенная комбинация текущего зашумлённого сэмпла $\mathbf{x}_t$ и чистого сэмпла $\mathbf{x}_0$. Веса определяются расписанием шума.

Собирая всё вместе, получаем замкнутую формулу:

$$q(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{x}_0) = \mathcal{N}\!\left(\tilde{\boldsymbol{\mu}}_t(\mathbf{x}_t, \mathbf{x}_0),\; \tilde{\beta}_t \cdot \mathbf{I}\right)$$

**Физический смысл.** Это распределение описывает, как правильно «денойзить» изображение $\mathbf{x}_t$ на один шаг назад, **если мы знаем оригинальное чистое изображение** $\mathbf{x}_0$. Среднее $\tilde{\boldsymbol{\mu}}_t$ интерполирует между зашумлённым наблюдением $\mathbf{x}_t$ и чистым сигналом $\mathbf{x}_0$, а дисперсия $\tilde{\beta}_t$ отражает неопределённость одного шага обратного перехода.

![[images/ddpm/1cb075ec-2b8a-4a8a-b1d2-52c1ff3a53ce.gif]]

### Сравнение трёх распределений

Подведём итог всех распределений, связанных с обратным процессом:

|Распределение|Формула|Статус|
|---|---|---|
|$q(\mathbf{x}_t \mid \mathbf{x}_{t-1})$ — прямой переход|$\mathcal{N}(\sqrt{\alpha_t} \cdot \mathbf{x}_{t-1},\, \beta_t \mathbf{I})$|Известно|
|$q(\mathbf{x}_{t-1} \mid \mathbf{x}_t)$ — обратный переход|$\frac{q(\mathbf{x}_t \mid \mathbf{x}_{t-1})\, q(\mathbf{x}_{t-1})}{q(\mathbf{x}_t)} \approx \mathcal{N}\!\left(\boldsymbol{\mu}_{\theta,t}(\mathbf{x}_t),\, \sigma^2_{\theta,t}(\mathbf{x}_t) \cdot \mathbf{I}\right)$|Неразрешим, аппроксимируем|
|$q(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{x}_0)$ — условный обратный переход|$\mathcal{N}\!\left(\tilde{\boldsymbol{\mu}}_t(\mathbf{x}_t, \mathbf{x}_0),\, \tilde{\beta}_t \mathbf{I}\right)$|Известен в замкнутом виде|

Второе распределение — то, что мы хотим приблизить нейронной сетью. Третье — то, что мы можем вычислить аналитически при известном $\mathbf{x}_0$. Именно третье распределение станет «учительским сигналом» при обучении: мы будем минимизировать расхождение между обучаемым $p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t)$ и истинным $q(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{x}_0)$, что приведёт нас к формулировке ELBO.

## Gaussian Diffusion Model as VAE

Мы вывели три ключевых распределения и указали, что обучение модели сведётся к минимизации расхождения между обучаемым $p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t)$ и истинным $q(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{x}_0)$. Но как формализовать эту идею? Как вывести целевую функцию, которую можно оптимизировать градиентным спуском? Для этого нам придётся взглянуть на диффузию под другим углом — как на модель латентной переменной.

### Latent variable model

Начнём с общей постановки, не привязанной ни к VAE, ни к диффузии. Пусть $\mathbf{x}$ — наблюдаемая переменная (например, изображение), а $\mathbf{z}$ — скрытая (латентная) переменная, которую мы не наблюдаем напрямую. Совместное распределение разлагается как:

$$p_\theta(\mathbf{x}, \mathbf{z}) = p_\theta(\mathbf{x} \mid \mathbf{z}) \cdot p_\theta(\mathbf{z})$$

Наша цель — максимизировать маргинальное логарифмическое правдоподобие:

$$\log p_\theta(\mathbf{x}) = \log \int p_\theta(\mathbf{x}, \mathbf{z}) \, d\mathbf{z}$$

Проблема в том, что этот интеграл берётся по всем возможным значениям $\mathbf{z}$. Если латентное пространство высокоразмерно — а оно, как правило, таково — прямое вычисление интеграла неразрешимо.

Теперь заметим, что диффузионная модель — это именно такая латентно-переменная модель. Наблюдаемая переменная — чистое изображение $\mathbf{x}_0 \sim p_{\text{data}}(\mathbf{x})$, а латентная переменная — вся цепочка зашумлённых версий:

$$\mathbf{z} = (\mathbf{x}_1, \mathbf{x}_2, \ldots, \mathbf{x}_T)$$

Обратим внимание на необычную деталь: каждый $\mathbf{x}_t$ имеет ту же размерность, что и $\mathbf{x}_0$. Суммарная размерность латентного пространства — $T \cdot \dim(\mathbf{x}_0)$, что на порядки превышает размерность данных. Для изображения $256 \times 256 \times 3$ при $T = 1000$ это около $200$ миллионов скрытых переменных.

Итак, мы имеем наблюдаемые данные и гигантское пространство скрытых переменных. Мы хотим максимизировать правдоподобие, но не можем вычислить интеграл. Нам нужен обходной путь — и именно его предоставляет вариационный вывод.

### VAE: вариационная нижняя граница

Идея вариационного вывода: раз мы не можем точно вычислить апостериорное распределение $p_\theta(\mathbf{z} \mid \mathbf{x})$, введём его приближение $q(\mathbf{z} \mid \mathbf{x})$ и будем работать с ним. Можно показать, что для любого распределения $q(\mathbf{z} \mid \mathbf{x})$ выполняется неравенство:

$$\log p_\theta(\mathbf{x}) \geq \mathbb{E}_{q(\mathbf{z} \mid \mathbf{x})} \log \frac{p_\theta(\mathbf{x}, \mathbf{z})}{q(\mathbf{z} \mid \mathbf{x})} = \mathcal{L}(\mathbf{x}) \to \max_\theta$$

Эта нижняя граница называется **ELBO** (Evidence Lower Bound). Вместо того чтобы максимизировать неразрешимое правдоподобие, мы максимизируем ELBO — величину, которую можно оценить и оптимизировать.

В стандартном VAE эта схема реализуется через три компонента:

- **Энкодер** $q_\phi(\mathbf{z} \mid \mathbf{x})$ — нейронная сеть с параметрами $\phi$, приближающая апостериорное распределение $p_\theta(\mathbf{z} \mid \mathbf{x})$. По входному $\mathbf{x}$ предсказывает параметры распределения на $\mathbf{z}$.

- **Декодер** $p_\theta(\mathbf{x} \mid \mathbf{z})$ — нейронная сеть с параметрами $\theta$, восстанавливающая данные из латентного представления за один проход.

- **Приор** $p(\mathbf{z}) = \mathcal{N}(\mathbf{0}, \mathbf{I})$ — простое фиксированное распределение, не содержащее обучаемых параметров.

Энкодер и декодер обучаются совместно, максимизируя ELBO по параметрам $\phi$ и $\theta$. Теперь покажем, что диффузионная модель — это частный случай этой схемы, хотя и весьма необычный.

### Компоненты VAE в диффузионной модели

Определим каждый из трёх компонентов VAE в терминах диффузионного процесса.

**Энкодер** $q(\mathbf{z} \mid \mathbf{x})$ — прямой диффузионный процесс:

$$q(\mathbf{z} \mid \mathbf{x}) = q(\mathbf{x}_1, \ldots, \mathbf{x}_T \mid \mathbf{x}_0) = q(\mathbf{x}_1 \mid \mathbf{x}_0) \cdot q(\mathbf{x}_2 \mid \mathbf{x}_1, \mathbf{x}_0) \cdot q(\mathbf{x}_3 \mid \mathbf{x}_2, \mathbf{x}_1, \mathbf{x}_0) \cdots = \prod_{t=1}^{T} q(\mathbf{x}_t \mid \mathbf{x}_{t-1})$$

![[images/ddpm/7e4c4ff0-497b-49f6-bab8-67fac3fea446.png]]

Каждый переход $q(\mathbf{x}_t \mid \mathbf{x}_{t-1}) = \mathcal{N}(\sqrt{\alpha_t} \cdot \mathbf{x}_{t-1},\, \beta_t \mathbf{I})$ добавляет шум, постепенно превращая чистое изображение в белый шум. Принципиальное отличие от стандартного VAE: **энкодер не содержит обучаемых параметров**. Расписание шума $\{\beta_t\}_{t=1}^T$ задаётся заранее как гиперпараметр. В обычном VAE энкодер $q_\phi(\mathbf{z} \mid \mathbf{x})$ параметризуется нейронной сетью с весами $\phi$, которые оптимизируются совместно с декодером.

**Декодер** $p_\theta(\mathbf{x} \mid \mathbf{z})$ — один шаг денойзинга:

$$p_\theta(\mathbf{x} \mid \mathbf{z}) = p_\theta(\mathbf{x}_0 \mid\mathbf{x}_1, \ldots, \mathbf{x}_T) = p_\theta(\mathbf{x}_0 \mid \mathbf{x}_1)$$

Декодер использует только $\mathbf{x}_1$ — ближайшую к данным зашумлённую версию — и выполняет всего один шаг денойзинга. В стандартном VAE декодер отображает всё латентное представление $\mathbf{z}$ в пространство данных за один проход.

**Приор** $p_\theta(\mathbf{z})$ — обратная марковская цепь:

$$p_\theta(\mathbf{z}) = p_\theta(\mathbf{x}_1, \ldots, \mathbf{x}_T) = p(\mathbf{x}_T) \cdot \prod_{t=2}^{T} p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t)$$

![[images/ddpm/22ce7832-0c72-4bb0-a098-b8e71efdd45d.png]]

Здесь $p(\mathbf{x}_T) = \mathcal{N}(\mathbf{0}, \mathbf{I})$ — стартовая точка обратного процесса. В отличие от стандартного VAE, где приор — простое фиксированное распределение $\mathcal{N}(\mathbf{0}, \mathbf{I})$, здесь приор — целая марковская цепь с обучаемыми параметрами $\theta$. Сложность, которая в стандартном VAE целиком сосредоточена в декодере, здесь распределена между декодером и приором.

### Сравнение с обычным VAE

||Обычный VAE|Диффузионная модель|
|---|---|---|
|Латентное пространство|$\dim(\mathbf{z}) \ll \dim(\mathbf{x})$|$\dim(\mathbf{z}) = T \cdot \dim(\mathbf{x})$|
|Энкодер $q(\mathbf{z} \mid \mathbf{x})$|Нейросеть с параметрами $\phi$|Фиксированная марковская цепь|
|Декодер $p_\theta(\mathbf{x} \mid \mathbf{z})$|Нейросеть: $\mathbf{z} \to \mathbf{x}$ за один шаг|Один шаг: $p_\theta(\mathbf{x}_0 \mid \mathbf{x}_1)$|
|Приор $p(\mathbf{z})$|Простой: $\mathcal{N}(\mathbf{0}, \mathbf{I})$|Марковская цепь с параметрами $\theta$|
|Обучаемые параметры|Энкодер $\phi$ + декодер $\theta$|Только обратный процесс $\theta$|

Несмотря на эти различия, математический аппарат VAE — Evidence Lower Bound (ELBO) — применим напрямую. Установив соответствие между диффузией и VAE, мы теперь формально выведем целевую функцию обучения.

## ELBO for Gaussian Diffusion Model

### Стандартная формулировка

Записываем стандартное неравенство ELBO для латентно-переменной модели:

$$\log p_\theta(\mathbf{x}) \geq \mathbb{E}_{q(\mathbf{z} \mid \mathbf{x})} \log \frac{p_\theta(\mathbf{x}, \mathbf{z})}{q(\mathbf{z} \mid \mathbf{x})} = \mathcal{L}_{\phi,\theta}(\mathbf{x}) \to \max_{\phi, \theta}$$

Подставляя определения для диффузионной модели:

$$\mathcal{L}_{\phi,\theta}(\mathbf{x}) = \mathbb{E}_{q(\mathbf{x}_{1:T} \mid \mathbf{x}_0)} \log \frac{p_\theta(\mathbf{x}_0, \mathbf{x}_{1:T})}{q(\mathbf{x}_{1:T} \mid \mathbf{x}_0)}$$

Раскроем числитель и знаменатель, используя марковскую структуру:

$$\mathcal{L}_{\phi,\theta}(\mathbf{x}) = \mathbb{E}_{q(\mathbf{x}_{1:T} \mid \mathbf{x}_0)} \log \frac{p(\mathbf{x}_T) \displaystyle\prod_{t=1}^{T} p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t)}{\displaystyle\prod_{t=1}^{T} q(\mathbf{x}_t \mid \mathbf{x}_{t-1})}$$

Наша цель — разложить ELBO на сумму индивидуальных KL-дивергенций, каждую из которых можно вычислить аналитически. Для этого нам понадобится два ключевых приёма: обусловливание на $\mathbf{x}_0$ и телескопирование.

### Вывод ELBO

**Шаг 1: обусловливание на** $\mathbf{x}_0$**.** Прямые переходы $q(\mathbf{x}_t \mid \mathbf{x}_{t-1})$ не зависят от $\mathbf{x}_0$ в силу марковского свойства: зная $\mathbf{x}_{t-1}$, информация о $\mathbf{x}_0$ избыточна для предсказания $\mathbf{x}_t$. Поэтому:

$$q(\mathbf{x}_t \mid \mathbf{x}_{t-1}) = q(\mathbf{x}_t \mid \mathbf{x}_{t-1}, \mathbf{x}_0)$$

Это тождество, но оно позволяет в следующем шаге использовать формулу Байеса с участием $\mathbf{x}_0$, чтобы выразить прямые переходы через известные нам условные обратные.

**Шаг 2: замена прямых переходов на обратные.** Для $t \geq 2$ применим формулу Байеса:

$$q(\mathbf{x}_t \mid \mathbf{x}_{t-1}, \mathbf{x}_0) = \frac{q(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{x}_0) \cdot q(\mathbf{x}_t \mid \mathbf{x}_0)}{q(\mathbf{x}_{t-1} \mid \mathbf{x}_0)}$$

Подставим в знаменатель ELBO, выделив первый переход $q(\mathbf{x}_1 \mid \mathbf{x}_0)$ отдельно:

$$\prod_{t=1}^{T} q(\mathbf{x}_t \mid \mathbf{x}_{t-1}) = q(\mathbf{x}_1 \mid \mathbf{x}_0) \cdot \prod_{t=2}^{T} \frac{q(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{x}_0) \cdot q(\mathbf{x}_t \mid \mathbf{x}_0)}{q(\mathbf{x}_{t-1} \mid \mathbf{x}_0)}$$

**Шаг 3: телескопирование.** Произведение дробей $q(\mathbf{x}_t \mid \mathbf{x}_0) / q(\mathbf{x}_{t-1} \mid \mathbf{x}_0)$ является телескопическим:

$$\prod_{t=2}^{T} \frac{q(\mathbf{x}_t \mid \mathbf{x}_0)}{q(\mathbf{x}_{t-1} \mid \mathbf{x}_0)} = \frac{q(\mathbf{x}_T \mid \mathbf{x}_0)}{q(\mathbf{x}_1 \mid \mathbf{x}_0)}$$

Действительно, если расписать произведение:

$$\frac{q(\mathbf{x}_2 \mid \mathbf{x}_0)}{q(\mathbf{x}_1 \mid \mathbf{x}_0)} \cdot \frac{q(\mathbf{x}_3 \mid \mathbf{x}_0)}{q(\mathbf{x}_2 \mid \mathbf{x}_0)} \cdot \ldots \cdot \frac{q(\mathbf{x}_T \mid \mathbf{x}_0)}{q(\mathbf{x}_{T-1} \mid \mathbf{x}_0)}$$

все промежуточные члены сокращаются. Подставляя и сокращая $q(\mathbf{x}_1 \mid \mathbf{x}_0)$, получаем компактную форму знаменателя:

$$\prod_{t=1}^{T} q(\mathbf{x}_t \mid \mathbf{x}_{t-1}) = q(\mathbf{x}_T \mid \mathbf{x}_0) \cdot \prod_{t=2}^{T} q(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{x}_0)$$

**Шаг 4: подстановка в ELBO.** Подставляем упрощённый знаменатель и раскрываем числитель как $p(\mathbf{x}_T) \cdot p_\theta(\mathbf{x}_0 \mid \mathbf{x}_1) \cdot \prod_{t=2}^{T} p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t)$:

$$\mathcal{L}_{\phi,\theta}(\mathbf{x}) = \mathbb{E}_{q(\mathbf{x}_{1:T} \mid \mathbf{x}_0)} \log \frac{p(\mathbf{x}_T) \cdot p_\theta(\mathbf{x}_0 \mid \mathbf{x}_1) \cdot \displaystyle\prod_{t=2}^{T} p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t)}{q(\mathbf{x}_T \mid \mathbf{x}_0) \cdot \displaystyle\prod_{t=2}^{T} q(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{x}_0)}$$

Разделяем логарифм произведения на сумму логарифмов:

$$= \mathbb{E}_{q(\mathbf{x}_{1:T} \mid \mathbf{x}_0)} \left[ \log p_\theta(\mathbf{x}_0 \mid \mathbf{x}_1) + \log \frac{p(\mathbf{x}_T)}{q(\mathbf{x}_T \mid \mathbf{x}_0)} + \sum_{t=2}^{T} \log \frac{p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t)}{q(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{x}_0)} \right]$$

Наконец, выносим ожидания по нужным маргиналам и записываем логарифмы дробей через KL-дивергенции. Получаем финальное разложение ELBO:

$$\boxed{\mathcal{L}_{\phi,\theta}(\mathbf{x}) = \underbrace{\mathbb{E}_{q(\mathbf{x}_1 \mid \mathbf{x}_0)} \log p_\theta(\mathbf{x}_0 \mid \mathbf{x}_1)}_{\text{reconstruction}} - \underbrace{D_{\text{KL}}\!\left(q(\mathbf{x}_T \mid \mathbf{x}_0) \,\|\, p(\mathbf{x}_T)\right)}_{\text{prior matching}} - \sum_{t=2}^{T} \underbrace{\mathbb{E}_{q(\mathbf{x}_t \mid \mathbf{x}_0)}\, D_{\text{KL}}\!\left(q(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{x}_0) \,\|\, p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t)\right)}_{\mathcal{L}_t}}$$

### Анализ слагаемых

Разберём каждое слагаемое ELBO:

**Первое слагаемое: reconstruction.** Логарифм правдоподобия декодера:

$$\mathbb{E}_{q(\mathbf{x}_1 \mid \mathbf{x}_0)} \log p_\theta(\mathbf{x}_0 \mid \mathbf{x}_1) = \mathbb{E}_{q(\mathbf{x}_1 \mid \mathbf{x}_0)} \log \mathcal{N}\!\left(\mathbf{x}_0 \mid \boldsymbol{\mu}_{\theta,1}(\mathbf{x}_1),\, \sigma^2_{\theta,1}(\mathbf{x}_1) \cdot \mathbf{I}\right)$$

Это стандартная реконструкция из VAE: насколько хорошо модель восстанавливает чистое изображение $\mathbf{x}_0$ из слегка зашумлённого $\mathbf{x}_1 \sim q(\mathbf{x}_1 \mid \mathbf{x}_0)$.

**Второе слагаемое: prior matching.** KL-дивергенция между конечным состоянием прямого процесса и приором:

$$D_{\text{KL}}\!\left(q(\mathbf{x}_T \mid \mathbf{x}_0) \,\|\, p(\mathbf{x}_T)\right) = D_{\text{KL}}\!\left(\mathcal{N}\!\left(\sqrt{\bar{\alpha}_T} \cdot \mathbf{x}_0,\, (1 - \bar{\alpha}_T) \mathbf{I}\right) \,\|\, \mathcal{N}(\mathbf{0}, \mathbf{I})\right)$$

Это слагаемое — **константа**: оба распределения полностью определены (расписание шума фиксировано, $\mathbf{x}_0$ задано), обучаемых параметров $\theta$ здесь нет. При $\bar{\alpha}_T \approx 0$ (что обеспечивается расписанием шума при большом $T$) $q(\mathbf{x}_T \mid \mathbf{x}_0) \approx \mathcal{N}(\mathbf{0}, \mathbf{I}) = p(\mathbf{x}_T)$, и KL-дивергенция стремится к нулю.

**Третье слагаемое: denoising matching** $\mathcal{L}_t$**.** Это основной вклад в ELBO:

$$\mathcal{L}_t = \mathbb{E}_{q(\mathbf{x}_t \mid \mathbf{x}_0)}\, D_{\text{KL}}\!\left(q(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{x}_0) \,\|\, p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t)\right)$$

Для каждого шага $t$ мы минимизируем KL-дивергенцию между двумя гауссианами:

- **«Учитель»**: $q(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{x}_0) = \mathcal{N}\!\left(\tilde{\boldsymbol{\mu}}_t(\mathbf{x}_t, \mathbf{x}_0),\, \tilde{\beta}_t \mathbf{I}\right)$ — истинный условный обратный переход, известный в замкнутом виде.

- **«Ученик»**: $p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t) = \mathcal{N}\!\left(\boldsymbol{\mu}_{\theta,t}(\mathbf{x}_t),\, \sigma^2_{\theta,t}(\mathbf{x}_t) \cdot \mathbf{I}\right)$ — обучаемый обратный переход.

Интуитивно, на каждом шаге модель учится делать денойзинг так же, как это делает оптимальный обратный переход при известном $\mathbf{x}_0$.

### Упрощение $\mathcal{L}_t$: фиксация дисперсии

Авторы DDPM (Ho et al., 2020) предлагают зафиксировать дисперсию обучаемого обратного перехода:

$$\sigma^2_{\theta,t}(\mathbf{x}_t) = \tilde{\beta}_t \quad \Rightarrow \quad p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t) = \mathcal{N}\!\left(\boldsymbol{\mu}_{\theta,t}(\mathbf{x}_t),\, \tilde{\beta}_t \cdot \mathbf{I}\right)$$

Это обосновано тем, что оптимальная дисперсия $\sigma^2_{\theta,t}$ теоретически лежит в интервале $[\tilde{\beta}_t, \beta_t]$. Интуиция: дисперсия обратного шага складывается из «неустранимого» шума $\tilde{\beta}_t$ (присутствует даже при известном $\mathbf{x}_0$) и неопределённости в том, какое именно $\mathbf{x}_0$ породило наблюдаемый $\mathbf{x}_t$. Если датасет состоит из единственного изображения ($p_{\text{data}} = \delta(\mathbf{x}_0 - \mathbf{x}^*)$), неопределённости нет и дисперсия минимальна — $\tilde{\beta}_t$. В теоретическом пределе максимальной неопределённости ($p_{\text{data}} = \mathcal{N}(\mathbf{0}, \mathbf{I})$ — не реальные данные, а крайний случай для получения верхней границы) дисперсия достигает $\beta_t$. Поскольку оба предела малы ($\beta_t \ll 1$), конкретный выбор внутри интервала практически не влияет на качество.

При совпадающих дисперсиях KL-дивергенция между двумя гауссианами сводится к нормированному расстоянию между средними:

$$D_{\text{KL}}\!\left(\mathcal{N}(\tilde{\boldsymbol{\mu}}_t, \tilde{\beta}_t \mathbf{I}) \,\|\, \mathcal{N}(\boldsymbol{\mu}_{\theta,t}, \tilde{\beta}_t \mathbf{I})\right) = \frac{1}{2\tilde{\beta}_t} \left\| \tilde{\boldsymbol{\mu}}_t(\mathbf{x}_t, \mathbf{x}_0) - \boldsymbol{\mu}_{\theta,t}(\mathbf{x}_t) \right\|^2$$

Таким образом, каждое слагаемое $\mathcal{L}_t$ принимает вид:

$$\mathcal{L}_t = \mathbb{E}_{q(\mathbf{x}_t \mid \mathbf{x}_0)} \left[ \frac{1}{2\tilde{\beta}_t} \left\| \tilde{\boldsymbol{\mu}}_t(\mathbf{x}_t, \mathbf{x}_0) - \boldsymbol{\mu}_{\theta,t}(\mathbf{x}_t) \right\|^2 \right]$$

Задача обучения свелась к MSE между средними: модель должна предсказать среднее истинного условного обратного перехода $\tilde{\boldsymbol{\mu}}_t(\mathbf{x}_t, \mathbf{x}_0)$, имея на вход только зашумлённый сэмпл $\mathbf{x}_t$.

### Обучение и сэмплирование

Собирая всё вместе: prior matching — константа, стремящаяся к нулю (показано выше), и мы его отбрасываем. Остаётся показать, что reconstruction-слагаемое — это частный случай MSE-слагаемого при $t = 1$.

Reconstruction-слагаемое при фиксированной дисперсии $\tilde{\beta}_1$:

$$\mathbb{E}_{q(\mathbf{x}_1 \mid \mathbf{x}_0)} \log p_\theta(\mathbf{x}_0 \mid \mathbf{x}_1) = \mathbb{E}_{q(\mathbf{x}_1 \mid \mathbf{x}_0)} \log \mathcal{N}\!\left(\mathbf{x}_0 \mid \boldsymbol{\mu}_{\theta,1}(\mathbf{x}_1),\, \tilde{\beta}_1 \mathbf{I}\right) = -\frac{1}{2\tilde{\beta}_1} \mathbb{E}_{q(\mathbf{x}_1 \mid \mathbf{x}_0)} \left\| \mathbf{x}_0 - \boldsymbol{\mu}_{\theta,1}(\mathbf{x}_1) \right\|^2 + \text{const}$$

Подставим $t = 1$ в формулу для $\tilde{\boldsymbol{\mu}}_t$. По соглашению $\bar{\alpha}_0 = 1$, поэтому:

$$\tilde{\boldsymbol{\mu}}_1(\mathbf{x}_1, \mathbf{x}_0) = \frac{\sqrt{\alpha_1}\overbrace{(1 - \bar{\alpha}_0)}^{= \, 0}}{1 - \bar{\alpha}_1} \cdot \mathbf{x}_1 + \frac{\overbrace{\sqrt{\bar{\alpha}_0}}^{= \, 1}(1 - \alpha_1)}{1 - \bar{\alpha}_1} \cdot \mathbf{x}_0 = \frac{1 - \alpha_1}{1 - \alpha_1} \cdot \mathbf{x}_0 = \mathbf{x}_0$$

Таким образом, $\|\mathbf{x}_0 - \boldsymbol{\mu}_{\theta,1}\|^2 = \|\tilde{\boldsymbol{\mu}}_1(\mathbf{x}_1, \mathbf{x}_0) - \boldsymbol{\mu}_{\theta,1}(\mathbf{x}_1)\|^2$, и reconstruction-слагаемое совпадает с MSE-слагаемым $\mathcal{L}_1$. ELBO сворачивается в единую сумму:

$$\mathcal{L}_\theta(\mathbf{x}) = - \sum_{t=1}^{T} \mathbb{E}_{q(\mathbf{x}_t \mid \mathbf{x}_0)} \left[ \frac{1}{2\tilde{\beta}_t} \left\| \tilde{\boldsymbol{\mu}}_t(\mathbf{x}_t, \mathbf{x}_0) - \boldsymbol{\mu}_{\theta,t}(\mathbf{x}_t) \right\|^2 \right]$$

**Алгоритм обучения:**

1. Получить сэмпл $\mathbf{x}_0 \sim p_{\text{data}}(\mathbf{x})$

1. Сгенерировать зашумлённое изображение $\mathbf{x}_t = \sqrt{\bar{\alpha}_t} \cdot \mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t} \cdot \boldsymbol{\epsilon}$, где $\boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$

1. Вычислить ELBO и обновить параметры $\theta$

**Алгоритм сэмплирования (ancestral sampling):**

1. Сэмплировать $\mathbf{x}_T \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$

1. Для $t = T, T-1, \ldots, 1$ выполнить денойзинг: $\mathbf{x}_{t-1} = \boldsymbol{\mu}_{\theta,t}(\mathbf{x}_t) + \sqrt{\tilde{\beta}_t} \cdot \boldsymbol{\epsilon}$, где $\boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$

На данном этапе задача обучения полностью определена: модель $\boldsymbol{\mu}_{\theta,t}$ учится предсказывать среднее условного обратного перехода. Однако вспомним, что $\tilde{\boldsymbol{\mu}}_t$ зависит от $\mathbf{x}_0$, который при сэмплировании неизвестен. В следующем разделе мы покажем, как репараметризовать $\boldsymbol{\mu}_{\theta,t}$ так, чтобы модель предсказывала шум $\boldsymbol{\epsilon}$ вместо среднего — что приведёт к элегантной и практичной формулировке DDPM.

## Reparametrization

### Проблема: зависимость от $\mathbf{x}_0$

Вернёмся к слагаемому $\mathcal{L}_t$, составляющему основной вклад в ELBO:

$$\mathcal{L}_t = \mathbb{E}_{q(\mathbf{x}_t \mid \mathbf{x}_0)} \left[ \frac{1}{2\tilde{\beta}_t} \left\| \tilde{\boldsymbol{\mu}}_t(\mathbf{x}_t, \mathbf{x}_0) - \boldsymbol{\mu}_{\theta,t}(\mathbf{x}_t) \right\|^2 \right]$$

Целевое среднее $\tilde{\boldsymbol{\mu}}_t(\mathbf{x}_t, \mathbf{x}_0)$ зависит от чистого изображения $\mathbf{x}_0$, которое при генерации нам недоступно. Модель же $\boldsymbol{\mu}_{\theta,t}(\mathbf{x}_t)$ принимает на вход только зашумлённый сэмпл $\mathbf{x}_t$. Возникает вопрос: как устранить зависимость от $\mathbf{x}_0$ и переформулировать задачу в терминах величин, доступных модели?

Ключевое наблюдение: между $\mathbf{x}_0$, $\mathbf{x}_t$ и шумом $\boldsymbol{\epsilon}$ существует линейная связь. Из замкнутой формулы прямого перехода:

$$\mathbf{x}_t = \sqrt{\bar{\alpha}_t} \cdot \mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t} \cdot \boldsymbol{\epsilon}, \quad \boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$$

мы можем выразить $\mathbf{x}_0$ через $\mathbf{x}_t$ и $\boldsymbol{\epsilon}$:

$$\mathbf{x}_0 = \frac{\mathbf{x}_t - \sqrt{1 - \bar{\alpha}_t} \cdot \boldsymbol{\epsilon}}{\sqrt{\bar{\alpha}_t}}$$

Это позволит переписать $\tilde{\boldsymbol{\mu}}_t$ как функцию только $\mathbf{x}_t$ и $\boldsymbol{\epsilon}$ — и мотивировать нейронную сеть предсказывать шум $\boldsymbol{\epsilon}$ вместо среднего.

### Перепараметризация $\tilde{\boldsymbol{\mu}}_t$

Подставим выражение для $\mathbf{x}_0$ в формулу среднего:

$$\tilde{\boldsymbol{\mu}}_t(\mathbf{x}_t, \mathbf{x}_0) = \frac{\sqrt{\alpha_t}(1 - \bar{\alpha}_{t-1})}{1 - \bar{\alpha}_t} \cdot \mathbf{x}_t + \frac{\sqrt{\bar{\alpha}_{t-1}}(1 - \alpha_t)}{1 - \bar{\alpha}_t} \cdot \mathbf{x}_0$$

Заменяем $\mathbf{x}_0$:

$$\tilde{\boldsymbol{\mu}}_t(\mathbf{x}_t, \boldsymbol{\epsilon}) = \frac{\sqrt{\alpha_t}(1 - \bar{\alpha}_{t-1})}{1 - \bar{\alpha}_t} \cdot \mathbf{x}_t + \frac{\sqrt{\bar{\alpha}_{t-1}}(1 - \alpha_t)}{1 - \bar{\alpha}_t} \cdot \frac{\mathbf{x}_t - \sqrt{1 - \bar{\alpha}_t} \cdot \boldsymbol{\epsilon}}{\sqrt{\bar{\alpha}_t}}$$

Раскроем второе слагаемое, воспользовавшись тем, что $\frac{\sqrt{\bar{\alpha}_{t-1}}}{\sqrt{\bar{\alpha}_t}} = \frac{1}{\sqrt{\alpha_t}}$ (поскольку $\bar{\alpha}_t = \alpha_t \cdot \bar{\alpha}_{t-1}$):

$$= \frac{\sqrt{\alpha_t}(1 - \bar{\alpha}_{t-1})}{1 - \bar{\alpha}_t} \cdot \mathbf{x}_t + \frac{(1 - \alpha_t)}{(1 - \bar{\alpha}_t)\sqrt{\alpha_t}} \cdot \mathbf{x}_t - \frac{(1 - \alpha_t)\sqrt{1 - \bar{\alpha}_t}}{(1 - \bar{\alpha}_t)\sqrt{\alpha_t}} \cdot \boldsymbol{\epsilon}$$

Соберём коэффициент при $\mathbf{x}_t$, приведя к общему знаменателю $(1 - \bar{\alpha}_t)\sqrt{\alpha_t}$:

$$\frac{\sqrt{\alpha_t}(1 - \bar{\alpha}_{t-1})}{1 - \bar{\alpha}_t} + \frac{1 - \alpha_t}{(1 - \bar{\alpha}_t)\sqrt{\alpha_t}} = \frac{\alpha_t(1 - \bar{\alpha}_{t-1}) + (1 - \alpha_t)}{(1 - \bar{\alpha}_t)\sqrt{\alpha_t}}$$

Числитель упрощается точно так же, как в выводе $\tilde{\beta}_t$:

$$\alpha_t(1 - \bar{\alpha}_{t-1}) + (1 - \alpha_t) = \alpha_t - \underbrace{\alpha_t \bar{\alpha}_{t-1}}_{=\,\bar{\alpha}_t} + 1 - \alpha_t = 1 - \bar{\alpha}_t$$

Коэффициент при $\boldsymbol{\epsilon}$ упрощается сокращением $\sqrt{1 - \bar{\alpha}_t}$:

$$\frac{(1 - \alpha_t)\sqrt{1 - \bar{\alpha}_t}}{(1 - \bar{\alpha}_t)\sqrt{\alpha_t}} = \frac{1 - \alpha_t}{\sqrt{1 - \bar{\alpha}_t} \cdot \sqrt{\alpha_t}}$$

Подставляя, получаем компактную формулу:

$$\boxed{\tilde{\boldsymbol{\mu}}_t(\mathbf{x}_t, \boldsymbol{\epsilon}) = \frac{1}{\sqrt{\alpha_t}} \left( \mathbf{x}_t - \frac{1 - \alpha_t}{\sqrt{1 - \bar{\alpha}_t}} \cdot \boldsymbol{\epsilon} \right)}$$

Эта формула замечательна своей простотой: среднее обратного перехода — это масштабированный $\mathbf{x}_t$ с вычтенной «долей шума». Коэффициент $\frac{1}{\sqrt{\alpha_t}}$ компенсирует сжатие сигнала, выполненное прямым процессом, а слагаемое $\frac{1 - \alpha_t}{\sqrt{1 - \bar{\alpha}_t}} \cdot \boldsymbol{\epsilon}$ — ту часть шума, которую нужно удалить.

### Параметризация модели через предсказание шума

Формула для $\tilde{\boldsymbol{\mu}}_t$ подсказывает естественную параметризацию обучаемого среднего $\boldsymbol{\mu}_{\theta,t}$. Поскольку $\mathbf{x}_t$ — входное значение, известное модели, единственная «неизвестная» в формуле — это шум $\boldsymbol{\epsilon}$. Заменим его на предсказание нейронной сети:

$$\boldsymbol{\mu}_{\theta,t}(\mathbf{x}_t) = \frac{1}{\sqrt{\alpha_t}} \left( \mathbf{x}_t - \frac{1 - \alpha_t}{\sqrt{1 - \bar{\alpha}_t}} \cdot \boldsymbol{\epsilon}_{\theta,t}(\mathbf{x}_t) \right)$$

где $\boldsymbol{\epsilon}_{\theta,t}(\mathbf{x}_t)$ — нейронная сеть с параметрами $\theta$, которая по зашумлённому сэмплу $\mathbf{x}_t$ предсказывает шум $\boldsymbol{\epsilon}$, добавленный прямым процессом. Вместо того чтобы напрямую предсказывать среднее (что требовало бы знания $\mathbf{x}_0$), модель решает задачу распознавания шума — определяет, какой именно гауссовский шум был добавлен к чистому изображению.

### Лосс в терминах шума

Подставим обе формулы в $\mathcal{L}_t$. Разность средних:

$$\tilde{\boldsymbol{\mu}}_t - \boldsymbol{\mu}_{\theta,t} = \frac{1}{\sqrt{\alpha_t}} \left( \mathbf{x}_t - \frac{1 - \alpha_t}{\sqrt{1 - \bar{\alpha}_t}} \cdot \boldsymbol{\epsilon} \right) - \frac{1}{\sqrt{\alpha_t}} \left( \mathbf{x}_t - \frac{1 - \alpha_t}{\sqrt{1 - \bar{\alpha}_t}} \cdot \boldsymbol{\epsilon}_{\theta,t}(\mathbf{x}_t) \right) = \frac{1 - \alpha_t}{\sqrt{\alpha_t(1 - \bar{\alpha}_t)}} \left( \boldsymbol{\epsilon}_{\theta,t}(\mathbf{x}_t) - \boldsymbol{\epsilon} \right)$$

Возведём в квадрат нормы и подставим в $\mathcal{L}_t$:

$$\mathcal{L}_t = \mathbb{E}_{q(\mathbf{x}_t \mid \mathbf{x}_0)} \left[ \frac{(1 - \alpha_t)^2}{2\tilde{\beta}_t \cdot \alpha_t (1 - \bar{\alpha}_t)} \left\| \boldsymbol{\epsilon} - \boldsymbol{\epsilon}_{\theta,t}(\mathbf{x}_t) \right\|^2 \right]$$

Перепишем ожидание по $q(\mathbf{x}_t \mid \mathbf{x}_0)$ как ожидание по $\boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$, поскольку сэмплирование $\mathbf{x}_t \sim q(\mathbf{x}_t \mid \mathbf{x}_0)$ эквивалентно сэмплированию $\boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ с последующей подстановкой $\mathbf{x}_t = \sqrt{\bar{\alpha}_t} \cdot \mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t} \cdot \boldsymbol{\epsilon}$:

$$\mathcal{L}_t = \mathbb{E}_{\boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})} \left[ \frac{(1 - \alpha_t)^2}{2\tilde{\beta}_t \cdot \alpha_t (1 - \bar{\alpha}_t)} \left\| \boldsymbol{\epsilon} - \boldsymbol{\epsilon}_{\theta,t}\!\left(\sqrt{\bar{\alpha}_t} \cdot \mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t} \cdot \boldsymbol{\epsilon}\right) \right\|^2 \right]$$

Результат интуитивно прозрачен: **на каждом шаге обратного процесса модель пытается предсказать шум** $\boldsymbol{\epsilon}$**, который был использован в прямом диффузионном процессе**. Это в точности задача денойзинга — по зашумлённому изображению определить, что является шумом, а что сигналом.

### Связь с Denoising Score Matching

Эта формулировка не случайно напоминает DSM из раздела NCSN. Вспомним, что score условного распределения диффузионного процесса имеет вид:

$$\nabla_{\mathbf{x}_t} \log q(\mathbf{x}_t \mid \mathbf{x}_0) = -\frac{\boldsymbol{\epsilon}}{\sqrt{1 - \bar{\alpha}_t}}$$

Предсказание шума $\boldsymbol{\epsilon}_{\theta,t}(\mathbf{x}_t)$ напрямую связано с предсказанием score-функции:

$$\mathbf{s}_{\theta,t}(\mathbf{x}_t) = -\frac{\boldsymbol{\epsilon}_{\theta,t}(\mathbf{x}_t)}{\sqrt{1 - \bar{\alpha}_t}}$$

Таким образом, обучение DDPM — это обучение score-функции, но в удобной параметризации через предсказание шума. Два подхода — score matching (NCSN) и вариационный вывод (DDPM) — приводят к одной и той же задаче оптимизации, что подтверждает глубокую связь между ними.

### Упрощённая целевая функция (Simplified Objective)

Авторы DDPM (Ho et al., 2020) обнаружили, что на практике модель обучается лучше, если отбросить весовой коэффициент $\frac{(1 - \alpha_t)^2}{2\tilde{\beta}_t \cdot \alpha_t (1 - \bar{\alpha}_t)}$ перед MSE. Интуитивно, этот коэффициент придаёт больший вес шагам с малыми $t$ (где шум мал и предсказание «проще»), но на практике равномерное взвешивание всех шагов даёт лучшее качество генерации.

Упрощённая целевая функция:

$$\boxed{\mathcal{L}_{\text{simple}} = \mathbb{E}_{t \sim U\{1, T\}} \, \mathbb{E}_{\boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})} \left\| \boldsymbol{\epsilon} - \boldsymbol{\epsilon}_{\theta,t}\!\left(\sqrt{\bar{\alpha}_t} \cdot \mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t} \cdot \boldsymbol{\epsilon}\right) \right\|^2}$$

Здесь $t$ сэмплируется равномерно из $\{1, 2, \ldots, T\}$, что объединяет reconstruction-слагаемое и все denoising matching-слагаемые в единый лосс. Эта формула — сердце DDPM: предельно простая задача регрессии, в которой нейронная сеть учится предсказывать шум по зашумлённому изображению.

### Итоговые алгоритмы

**Алгоритм обучения (Training):**

1. Получить сэмпл $\mathbf{x}_0 \sim p_{\text{data}}(\mathbf{x})$

1. Сэмплировать $t \sim U\{1, T\}$ и $\boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$

1. Вычислить зашумлённое изображение $\mathbf{x}_t = \sqrt{\bar{\alpha}_t} \cdot \mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t} \cdot \boldsymbol{\epsilon}$

1. Выполнить шаг градиентного спуска по $\nabla_\theta \left\| \boldsymbol{\epsilon} - \boldsymbol{\epsilon}_{\theta,t}(\mathbf{x}_t) \right\|^2$

**Алгоритм сэмплирования (Sampling):**

1. Сэмплировать $\mathbf{x}_T \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$

1. Для $t = T, T-1, \ldots, 1$:
    
    - Сэмплировать $\boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ (при $t > 1$; при $t = 1$ положить $\boldsymbol{\epsilon} = \mathbf{0}$)
    
    - Вычислить $\mathbf{x}_{t-1} = \frac{1}{\sqrt{\alpha_t}} \left( \mathbf{x}_t - \frac{1 - \alpha_t}{\sqrt{1 - \bar{\alpha}_t}} \cdot \boldsymbol{\epsilon}_{\theta,t}(\mathbf{x}_t) \right) + \sqrt{\tilde{\beta}_t} \cdot \boldsymbol{\epsilon}$
    

1. Вернуть $\mathbf{x}_0$

Обратим внимание на шаг сэмплирования: при $t = 1$ шум не добавляется ($\boldsymbol{\epsilon} = \mathbf{0}$), поскольку $\mathbf{x}_0$ — это финальный результат генерации, и добавление шума на последнем шаге только ухудшило бы качество.

### Summary

Подведём итог всего материала:

1. **DDPM аппроксимирует обратный процесс гауссианами** — это обосновано теоремой Феллера при малых $\beta_t$.

1. **DDPM — это VAE с иерархией латентных переменных**, где энкодер фиксирован, а приор — обучаемая марковская цепь.

1. **ELBO раскладывается в сумму KL-дивергенций** между известными условными обратными переходами $q(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{x}_0)$ и обучаемыми $p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t)$.

1. **Репараметризация сводит задачу к предсказанию шума** — на каждом шаге модель предсказывает гауссовский шум $\boldsymbol{\epsilon}$, добавленный прямым процессом.

1. **Предсказание шума эквивалентно обучению score-функции** — DDPM (вариационный вывод) и NCSN (score matching) приходят к одной и той же задаче оптимизации.

1. **Сэмплирование требует** $T$ **последовательных проходов** через нейронную сеть, что является основным узким местом метода.