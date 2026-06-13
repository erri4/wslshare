$$
\newcommand{\notimplies}{\;\not\!\!\!\implies}
\Gamma\colon \mathbb C \longrightarrow \mathbb C
\\[0.2cm]\Gamma(z)\coloneqq\int_0^{\infty} t^{z - 1}e^{-t}dt\\[0.3cm]
\Gamma(z+1)=\int_0^{\infty}t^ze^{-t}dt
\\[0.2cm]\int t^ze^{-t}dt=t^z\cdot\int e^{-t}dt-
\int(t^z)'\cdot\left(\int e^{-t}dt\right)dt=\\[0.2cm]=-t^ze^{-t}-\int zt^{z-1}\cdot -e^{-t}dt=-t^ze^{-t}t+z\int t^{z-1}e^{-t}dt\\[0.4cm]
\left.\int t^ze^{-t}dt\right|_{t=0}=\\[0.3cm]=\left.\left(e^{-t}\cdot\int t^zdt-\int(e^t)'\cdot\left(\int t^zdt\right)dt\right)\right|_{t=0}=\\[0.3cm]
=\left. \left(\frac {t^{z+1}\cdot e^{-t}} {z + 1}\right)\right|_{t=0}-\left.\int-e^{-t}\cdot\frac {t^{z+1}} {z+1}dt\right|_{t=0}=\\[0.3cm]
=\left. \int\frac {t^{z+1}\cdot e^{-t}} {z+1}dt\right|_{t=0}=\frac 1 {z+1}\left.\int t^{z+1}\cdot e^{-t}dt \right|_{t=0}=\\[0.3cm]
=\lim_{h\rightarrow\infty}\left(\frac {z!} {(z+h)!}\cdot\left.\int t^{z+h}e^{-t}dt\right|_{t=0}\right)=\\[0.3cm]
=\lim_{h\rightarrow\infty}\left(\prod_{n=0}^h\frac 1 {z+n}\right)\cdot\lim_{h\rightarrow\infty}\left(\left.\int t^{z+h}e^{-t}dt\right|_{t=0}\right)=0\\[0.7cm]
\text {Side proof:}\\[0.2cm]
\left.\int g(t)dt\right|_{t=0}\coloneqq0\\[0.2cm]
\int_0^bg(t)dt=\left.\int g(t)dt\right|_{t=b} - 0=\left.\int g(t)dt\right|_{t=b}\\[1cm]
\Gamma (z+1)=\lim_{m\rightarrow\infty}\int_0^mt^ze^{-t}dt=\\[0.2cm]
=\lim_{m\rightarrow\infty}\left(-m^ze^{-m}+z\left.\int t^{z-1}e^{-t}dt\right|_{t=m}\right)=\\[0.3cm]
=\lim_{m\rightarrow\infty}z\left.\int t^{z-1}e^{-t}dt\right|_{t=m}=z\lim_{m\rightarrow\infty}\int_0^mt^{z-1}e^{-t}dt=\\[0.3cm]
=z\int_0^{\infty}t^{z-1}e^{-t}dt=z\Gamma(z)\\[1cm]
\Gamma(1)=\int_0^{\infty}t^{1-1}e^{-t}dt=\int_0^{\infty}e^{-t}dt=\\[0.2cm]
=\lim_{m\rightarrow\infty}\int_0^me^{-t}dt=\lim_{m\rightarrow\infty}\left(-e^{-m}+1\right)=1\\[1cm]
f\colon\N\longrightarrow\N\\
f(n)\coloneqq(n-1)!\\
(n-1)!\cdot n=n!\\
f(n+1)=n\cdot f(n)\\
f(1)=1=\Gamma(1)\\[0.3cm]
\text {Assume: } \Gamma(z)=f(z)\\
\Gamma(z+1)=\Gamma(z)\cdot z=f(z)\cdot z=f(z+1)\implies\\
\implies\forall n\in\N\colon\Gamma(n+1)=f(n+1)=n!
$$