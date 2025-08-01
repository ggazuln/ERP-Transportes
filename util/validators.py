from wtforms.validators import ValidationError

class RUTValidator:
    """
    Validador de RUT chileno para formularios WTForms.
    Verifica que el RUT tenga el formato correcto y que el dígito verificador sea válido.
    """
    def __call__(self, form, field):
        rut = field.data
        if not rut:
            return  # Campo vacío se valida aparte si es obligatorio

        rut = rut.upper().replace(".", "").replace("-", "")
        if len(rut) < 2 or not rut[:-1].isdigit() or rut[-1] not in "0123456789K":
            raise ValidationError("Formato de RUT inválido. Use el formato 12.345.678-9")

        cuerpo = rut[:-1]
        dv_ingresado = rut[-1]

        suma = 0
        multiplo = 2
        for c in reversed(cuerpo):
            suma += int(c) * multiplo
            multiplo = 2 if multiplo == 7 else multiplo + 1

        dv_calculado = 11 - (suma % 11)
        if dv_calculado == 11:
            dv_esperado = '0'
        elif dv_calculado == 10:
            dv_esperado = 'K'
        else:
            dv_esperado = str(dv_calculado)

        if dv_ingresado != dv_esperado:
            raise ValidationError("El dígito verificador del RUT no es válido.")
