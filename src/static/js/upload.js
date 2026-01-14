const extensoes_aceitas = [
    "txt",
    "docx",
    "pdf"
]


const inputArquivo = document.getElementById('arquivo')
const areaLista = document.querySelector(".listarArquivos")
const listagem = document.querySelector('.listagemArquivos')

const quantidadeP = document.querySelector('.quantidadeArquivos p')

const nomeETamanho = document.querySelectorAll('.nomeETamanho p')

const formatoP = document.querySelector('.formatoArquivo')

function renderizarArquivos(arquivos) {
    areaLista.hidden = false;
    quantidadeP.textContent = `(${arquivos.length})`;

    for (const arquivo of arquivos) {
        const item = document.createElement("div");
        item.classList.add("itemArquivo");

        const info = document.createElement("div");
        info.classList.add("informacoesArquivo");

        // img
        const img = document.createElement("img");
        img.src = "/static/img/paper-upload-svgrepo-com.svg";
        img.classList.add("imgPapelUpload");

        // nome e tamanho
        const nomeETamanho = document.createElement("div");
        nomeETamanho.classList.add("nomeETamanho");

        const pNome = document.createElement("p");
        pNome.textContent = arquivo.name;

        const pTamanho = document.createElement("p");
        pTamanho.classList.add("tamanhoArquivo");
        pTamanho.textContent = `${(arquivo.size / 1024).toFixed(1)} KB`;

        nomeETamanho.append(pNome, pTamanho);

        info.append(img, nomeETamanho);

        // extensão
        const infoFinal = document.createElement("div");
        infoFinal.classList.add("informacoesFinal");

        const pExt = document.createElement("p");


        pExt.classList.add("formatoArquivo");
        pExt.textContent = arquivo.name.split(".").pop().toUpperCase();

        // botão remover
        const btnRemover = document.createElement("img");
        btnRemover.src = "/static/img/close-sm-svgrepo-com.svg";
        btnRemover.classList.add("imgX");
        btnRemover.style.cursor = "pointer";


        btnRemover.addEventListener("click", () => {
            item.remove();

            const arquivosRestantes = document.querySelectorAll(".itemArquivo");
            atualizarBotao(arquivosRestantes)
        });


        
        infoFinal.append(pExt, btnRemover);

        item.append(info, infoFinal);
        listagem.appendChild(item);
        
        
    }

}



const dropArea = document.querySelector('.dropArea')

function validarArquivos(arquivos) {
    const arquivos_filtrados = []
    for (const arquivo of arquivos) {
        if (extensoes_aceitas.includes(arquivo.name.split(".").pop().toLowerCase())) {
            arquivos_filtrados.push(arquivo)
        }
    }
    return arquivos_filtrados
}


inputArquivo.addEventListener("change", () => {
    listagem.innerHTML = "";
    const arquivosFiltrados = validarArquivos(inputArquivo.files)
    if (arquivosFiltrados.length > 0) {
        renderizarArquivos(arquivosFiltrados);
        atualizarBotao(arquivosFiltrados);
    }
});

dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropArea.classList.add("dragAtivo");
});

dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("dragAtivo");
});

dropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    dropArea.classList.remove("dragAtivo");

    listagem.innerHTML = "";
    const arquivosFiltrados = validarArquivos(e.dataTransfer.files)
    if (arquivosFiltrados.length > 0) {
        renderizarArquivos(arquivosFiltrados);
        atualizarBotao(arquivosFiltrados);
    }
});


const btnEnviar = document.querySelector(".btnEnviar");

function atualizarBotao(arquivos) {
    const qtd = arquivos.length;
    if (qtd > 0) {
        btnEnviar.disabled = false;
        quantidadeP.textContent = `(${qtd})`;
        quantidadeP.hidden = false;
        btnEnviar.classList.add("ativo");
        btnEnviar.textContent = `Enviar (${arquivos.length}) Arquivo(s)`;
    } else {
        areaLista.hidden = true;
        btnEnviar.disabled = true;
        btnEnviar.classList.remove("ativo");
        btnEnviar.textContent = "Selecione pelo menos um arquivo válido";
    }
}

btnRemover.addEventListener("click", () => {
    item.remove();
    atualizarBotao(document.querySelectorAll(".itemArquivo"))
})






// const inputArquivo = document.getElementById('arquivo')

// inputArquivo.addEventListener("change", () => {
//     const arquivo = inputArquivo.files[0];
//     console.log("nome:", arquivo.name)
//     console.log("tipo:", arquivo.type)
    
// })

// exemplo simples de validação

// inputArquivo.addEventListener("change", () => {
//     const arquivo = inputArquivo.files[0];
//     const nome = arquivo.name.toLowerCase();

//     if (nome.endsWith(".pdf")) {
//         console.log('É pdf') 
//     } else {
//         console.log('Formato inválido')
//     }
// })