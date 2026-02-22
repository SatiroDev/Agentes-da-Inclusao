const textarea = document.querySelector('.areaInputChat textarea')

const maxHeight = 150

let sessionId = localStorage.getItem("session_id");

if (!sessionId) {
    sessionId = crypto.randomUUID();
    localStorage.setItem("session_id", sessionId);
}


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

const btnEnviar = document.querySelector(".btnEnviarMsg")

const chatArea = document.querySelector(".areaConversa")

window.addEventListener("DOMContentLoaded", async () => {
    const agente = document.body.dataset.agente;

    const formData = new FormData();
    formData.append("agente", agente)
    formData.append("session_id", sessionId)



    const res = await fetch("/api/chat/init", {
        method: "POST",
        body: formData
    });

    const data = await res.json();

    const msg = document.createElement("div");
    msg.classList.add("chatMsgConversa");
    msg.innerHTML = `
        <div class="markdown">
            ${marked.parse(data.resposta)}
        </div>
    `

    chatArea.appendChild(msg);
});


btnEnviar.addEventListener("click", async () => {
    const mensagem = textarea.value.trim();
    if (!mensagem) return;

    const usuarioMsgConversa = document.createElement("div")
    usuarioMsgConversa.classList.add("usuarioMsgConversa")
    usuarioMsgConversa.innerHTML = `<p>${mensagem}</p>`


    chatArea.appendChild(usuarioMsgConversa)

    textarea.value = ""


    const formData = new FormData()
    formData.append("mensagem", mensagem)
    formData.append("session_id", sessionId);

    const res = await fetch("/api/chat", {
        method: "POST",
        body: formData
    })

    const data = await res.json()
    console.log(data)

    const chatMsgConversa = document.createElement("div")
    chatMsgConversa.classList.add("chatMsgConversa")

    chatMsgConversa.innerHTML = `
        <div class="markdown">
            ${marked.parse(data.resposta)}
        </div>
    `

    // 🔹 Se a resposta indicar que a prova foi adaptada, mostra botão PDF
    // 🔹 Se o backend enviar o link do PDF
    if (data.pdf_url) {
        const btnPdf = document.createElement("button")
        btnPdf.textContent = "📄 Visualizar PDF"
        btnPdf.classList.add("btnPdf")

        btnPdf.addEventListener("click", () => {
            window.open(data.pdf_url, "_blank")
        })

        chatMsgConversa.appendChild(btnPdf)
    }





    chatArea.appendChild(chatMsgConversa)

    chatArea.scrollTop = chatArea.scrollHeight

})

function atualizarDimensoes() {
    if (window.innerWidth <= 768) {
        mainChat.classList.add('mobile')
    } else {
        mainChat.classList.remove('mobile')
    }
}

atualizarDimensoes()