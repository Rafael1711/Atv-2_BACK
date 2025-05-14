const API_URL = "http://127.0.0.1:8000/api/instruments/";

document.addEventListener("DOMContentLoaded", fetchInstruments);

// Cadastro de novo instrumento
document.getElementById("instrument-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = {
        name: document.getElementById("name").value,
        category: document.getElementById("category").value,
        price: document.getElementById("price").value,
        description: document.getElementById("description").value
    };

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'Erro ao cadastrar instrumento');
        }

        // Limpa o formulário
        e.target.reset();

        // Atualiza a lista
        await fetchInstruments();

        alert('Instrumento cadastrado com sucesso!');
    } catch (error) {
        console.error("Erro no cadastro:", error);
        alert(`Erro: ${error.message}`);
    }
});

// Listagem de instrumentos
async function fetchInstruments() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) throw new Error('Erro ao carregar instrumentos');

        const instruments = await response.json();

        const tableBody = document.getElementById("instrument-list");
        tableBody.innerHTML = instruments.map(instrument => `
            <tr>
                <td>${instrument.name}</td>
                <td>
                    <button onclick="viewInstrument(${instrument.id})">Ver</button>
                    <button onclick="editInstrument(${instrument.id})">Editar</button>
                    <button onclick="deleteInstrument(${instrument.id})">Deletar</button>
                </td>
            </tr>
        `).join("");
    } catch (error) {
        console.error("Erro:", error);
        document.getElementById("instrument-list").innerHTML = `
            <tr>
                <td colspan="2">Erro ao carregar instrumentos: ${error.message}</td>
            </tr>
        `;
    }
}

// Visualização
window.viewInstrument = async function (id) {
    try {
        const response = await fetch(`${API_URL}${id}/`);
        if (!response.ok) throw new Error('Instrumento não encontrado');

        const instrument = await response.json();

        document.getElementById("modal-title").textContent = instrument.name;
        document.getElementById("modal-details").innerHTML = `
            <p><strong>Categoria:</strong> ${instrument.category}</p>
            <p><strong>Preço:</strong> R$ ${instrument.price.toFixed(2)}</p>
            <p><strong>Descrição:</strong> ${instrument.description || 'Nenhuma'}</p>
        `;
        document.getElementById("modal").style.display = "block";
    } catch (error) {
        console.error("Erro:", error);
        alert(error.message);
    }
};

// Edição
window.editInstrument = async function (id) {
    try {
        const response = await fetch(`${API_URL}${id}/`);
        if (!response.ok) throw new Error('Instrumento não encontrado');

        const instrument = await response.json();

        document.getElementById("edit-name").value = instrument.name;
        document.getElementById("edit-category").value = instrument.category;
        document.getElementById("edit-price").value = instrument.price;
        document.getElementById("edit-description").value = instrument.description || '';

        document.getElementById("edit-form").onsubmit = async function (e) {
            e.preventDefault();

            try {
                const response = await fetch(`${API_URL}${id}/`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        name: document.getElementById("edit-name").value,
                        category: document.getElementById("edit-category").value,
                        price: document.getElementById("edit-price").value,
                        description: document.getElementById("edit-description").value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Erro ao atualizar');
                }

                document.getElementById("edit-modal").style.display = "none";
                await fetchInstruments();
                alert('Instrumento atualizado com sucesso!');
            } catch (error) {
                console.error("Erro na edição:", error);
                alert(`Erro: ${error.message}`);
            }
        };

        document.getElementById("edit-modal").style.display = "block";
    } catch (error) {
        console.error("Erro:", error);
        alert(error.message);
    }
};

// Exclusão
window.deleteInstrument = async function (id) {
    if (!confirm("Tem certeza que deseja deletar este instrumento?")) return;

    try {
        const response = await fetch(`${API_URL}${id}/`, {
            method: "DELETE"
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Erro ao deletar');
        }

        await fetchInstruments();
        alert('Instrumento deletado com sucesso!');
    } catch (error) {
        console.error("Erro:", error);
        alert(`Erro: ${error.message}`);
    }
};
// Fechar modais
const closeModalButtons = document.querySelectorAll('.close, .close-edit');

closeModalButtons.forEach(button => {
    button.addEventListener('click', () => {
        document.querySelectorAll('.modal').forEach(modal => {
            modal.style.display = 'none';
        });
    });
});

// Fechar ao clicar fora do modal
window.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        e.target.style.display = 'none';
    }
});