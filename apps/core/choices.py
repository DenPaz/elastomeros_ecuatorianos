from django.db import models
from django.utils.translation import gettext_lazy as _


class Gender(models.TextChoices):
    MALE = "MALE", _("Male")
    FEMALE = "FEMALE", _("Female")
    OTHER = "OTHER", _("Other")


class Province(models.TextChoices):
    AZUAY = "AZUAY", _("Azuay")
    BOLIVAR = "BOLIVAR", _("Bolívar")
    CANAR = "CANAR", _("Cañar")
    CARCHI = "CARCHI", _("Carchi")
    COTOPAXI = "COTOPAXI", _("Cotopaxi")
    CHIMBORAZO = "CHIMBORAZO", _("Chimborazo")
    EL_ORO = "EL_ORO", _("El Oro")
    ESMERALDAS = "ESMERALDAS", _("Esmeraldas")
    GUAYAS = "GUAYAS", _("Guayas")
    IMBABURA = "IMBABURA", _("Imbabura")
    LOJA = "LOJA", _("Loja")
    LOS_RIOS = "LOS_RIOS", _("Los Ríos")
    MANABI = "MANABI", _("Manabí")
    MORONA_SANTIAGO = "MORONA_SANTIAGO", _("Morona Santiago")
    NAPO = "NAPO", _("Napo")
    ORELLANA = "ORELLANA", _("Orellana")
    PICHINCHA = "PICHINCHA", _("Pichincha")
    PASTAZA = "PASTAZA", _("Pastaza")
    SANTA_ELENA = "SANTA_ELENA", _("Santa Elena")
    SANTO_DOMINGO_DE_LOS_TSACHILAS = (
        "SANTO_DOMINGO_DE_LOS_TSACHILAS",
        _("Santo Domingo de los Tsáchilas"),
    )
    SUCUMBIOS = "SUCUMBIOS", _("Sucumbíos")
    TUNGURAHUA = "TUNGURAHUA", _("Tungurahua")
    ZAMORA_CHINCHIPE = "ZAMORA_CHINCHIPE", _("Zamora Chinchipe")
