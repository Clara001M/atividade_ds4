function validarCadastroUsuario(event) {
    event.preventDefault();

    const form = document.getElementById('form-cadastrarUsuario');
    const senha = form.querySelector('[name="senha"]').value
    const confirma = form.querySelector('[name="confirma"]').value
    if (senha != confirma) {
        alert("As senhas não são idênticas!");
    } else {
        form.submit();
    }
}