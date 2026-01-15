const textarea = document.querySelector('.areaInputChat textarea')

const maxHeight = 150

textarea.addEventListener("input", () => {
    textarea.style.height = "auto";
    if (textarea.scrollHeight < maxHeight) {
        textarea.style.height = textarea.scrollHeight + "px"
        textarea.style.overflowY = "hidden"
    } else {
        textarea.style.height = maxHeight + "px";
        textarea.style.overflowY = "auto";
    }
})

const barraLateral = document.querySelector('.barraLateral')
const btnBarraLateral = document.querySelector('.btnBarraLateral')
const imgPainel = document.querySelector(".imgPainel")
const mainChat = document.querySelector(".mainChat")
let barraAtivada = false


btnBarraLateral.addEventListener("click", () => {
    if (barraAtivada) {
        barraLateral.classList.remove("aberta")
        barraAtivada = false
        imgPainel.src = "../static/img/pane-open-svgrepo-com.svg"

    } else {
        barraLateral.classList.add("aberta")
        barraAtivada = true
        imgPainel.src = "../static/img/pane-close-svgrepo-com.svg"
    }

})

function atualizarDimensoes() {
    if (window.innerWidth <= 768) {
        mainChat.classList.add('mobile')
    } else {
        mainChat.classList.remove('mobile')
    }
}

atualizarDimensoes()