<h1>medidas</h1>
 
px,percent,rem,vh,dvh,vw,em

<h1>referências</h1>

* [vh](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/length#vh)

Represents a percentage of the height of the viewport's initial containing block. 1vh is 1% of the viewport height. For example, if the viewport height is 300px, then a value of 70vh on a property will be 210px.

The respective viewport-percentage units for small, large, and dynamic viewport sizes are svh, lvh, and dvh. vh is equivalent to lvh, representing the viewport-percentage length unit based on the large viewport size.
* [rem](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/length#rem)

Represents the font-size of the root element (typically <html>). When used within the root element font-size, it represents its initial value. A common browser default is 16px, but user-defined preferences may modify this.

* [px](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/length#px)

One pixel. For screen displays, it traditionally represents one device pixel (dot). However, for printers and high-resolution screens, one CSS pixel implies multiple device pixels. 1px = 1in / 96.

---

<h1>Principais usos</h1>


* px - elementos gráficos, que não escalam com a fonte do usuário.
* percent - barra de senha do javascript.
* rem - tipografia, espaçamento, layout - fonte do usuário do browser.
* vh - utilizado como fallback - browsers antigos pré 2022 não entendem dvh.
* vw - utilizado com clamp faixa intermediaria para fluidez.
* em - utilizado em letter-spacing espaçamento sempre proporcional ao tamanho daquele texto.