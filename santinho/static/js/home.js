    $.mask.masks.aposta = {mask: '69-69-69-69-69-69-69-69-69-69-69-69-69-69-69'};
    $.mask.masks.numero = {mask: '6'};
    $('.apostas_feitas').setMask();
    $('#numero_de_acertos').setMask();
    $('.acertos button').click(function() {
        $('#numero_de_acertos').val($(this).text());
        $(this).parents('#form-resultado').submit();
    });
    function adicionaInput(limpando) {
        apostas++;
        var novoInput = $('.copia').eq(0).clone();
        novoInput.removeClass('copia');
        novoInput.find('input').addClass('apostas_feitas');
        novoInput.find('input').attr('id', "aposta_" + apostas);
        novoInput.find('label').attr('for', "aposta_" + apostas);
        if (limpando) {
            novoInput.find('.remove-input').remove();
            novoInput.find('.input-prepend').removeClass('input-prepend');
        }
        $('.inputs').append(novoInput);
        novoInput.find('input').setMask();
    }

    $('#adiciona-aposta').click(function() {
        adicionaInput();
    });
    $('.inputs').on('click', '.remove-input', function() {
        if ($('.inputs .control-group').length == 1) {
            $(this).parent().find('input').val('');
        }
        else {
            $(this).parents('.control-group').remove();
        }
    });
    $('#form-resultado').submit(function() {
        var valido = true;
        $('.control-group.error').removeClass('error');
        $('.apostas_feitas').each(function() {
            var $this = $(this);
            var numeros = $this.val().split('-');
            if (numeros.length < 6) {
                exibeErro('Poucos números', 'São necessários no mínimo 6 números para a aposta.');
                valido = false;
                $this.parents('.control-group').addClass('error');
                return false;
            }
            var anterior = "00";
            numeros.sort();
            for (var i =0; i < numeros.length; i++) {
                var numero = numeros[i];
                if (numero.length != 2) {
                    exibeErro('Formato inválido', 'Use números com dois algarismos Ex.: 03-04-12-34-45-60');
                    valido = false;
                    $this.parents('.control-group').addClass('error');
                    return false;
                }
                if (numero == "00") {
                    exibeErro('Número inválido', 'Não pode haver números menores que 01 na aposta.');
                    valido = false;
                    $this.parents('.control-group').addClass('error');
                    return false;
                }
                if (parseInt(numero) > 60) {
                    exibeErro('Número inválido', 'Não podem haver números maiores que 60 na aposta.');
                    valido = false;
                    $this.parents('.control-group').addClass('error');
                    return false;
                }
                if (numero == anterior) {
                    exibeErro('Número repetido', 'Não podem haver números repetidos na aposta.');
                    valido = false;
                    $this.parents('.control-group').addClass('error');
                    return false;
                }
                anterior = numero;
            }
        });
        return valido;
    });

    $('#limpar').click(limpaCampos);

    function limpaCampos() {
        $('.inputs').empty();
        $('#numero_de_acertos').val(4);
        adicionaInput(true);
    }

    $('.inputs').on('click', '.tabela li', function(ev) {
        ev.stopPropagation();
        var $li = $(this);
        var aposta = $li.text();
        var input = $li.parents('.controls').find('.apostas_feitas');
        var numerosMarcados = parseInt(input.data('numerosMarcados'));
        var aposta_atual = input.val();
        if ($li.hasClass('marcado')) {
            aposta_atual = aposta_atual.split("-");
            var index = aposta_atual.indexOf(aposta);
            aposta_atual.splice(index, 1);
            input.val(aposta_atual.join("-"));
            $li.removeClass('marcado');
            input.data('numerosMarcados', --numerosMarcados);
            return false;
        }
        if (numerosMarcados == 15) {
            return false;
        }
        if (aposta_atual != "") {
            aposta = aposta_atual + "-" + aposta
        }
        input.val(aposta);
        $li.addClass('marcado');
        input.data('numerosMarcados', ++numerosMarcados);
    });

    $('.inputs').on('click', '.dropdown-toggle', function() {
        var input = $(this).parents('.controls').find('.apostas_feitas');
        var numeros = input.val();
        $(this).parent().find('.tabela li').removeClass("marcado");
        numeros = numeros.split("-");
        input.data('numerosMarcados', numeros.length);
        $(this).parent().find('.tabela li').each(function() {
            var $li = $(this);
            for (var i = 0; i < numeros.length; i++) {
                if ($li.text() == numeros[i]) {
                    $li.addClass('marcado');
                }
            }
        });
    });

    function exibeErro(titulo, mensagem) {
        $('.alert-error h4').text(titulo);
        $('.alert-error span').text(mensagem);
        $('.alert-error').removeClass('escondido');
    }

    $("#mostrar").click(function() {
        $("#form-resultado").attr("action", "/resultado/");
        $("#form-resultado").submit();
    });