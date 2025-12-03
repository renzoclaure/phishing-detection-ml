import re
import urllib.parse
import tldextract

def extract_url_features(url: str) -> dict:
    if not isinstance(url, str):
        url = str(url)
    url = url.strip()

    parsed = urllib.parse.urlparse(url)
    hostname = parsed.hostname or ""
    path = parsed.path or ""

    domain_info = tldextract.extract(url)
    subdomain = domain_info.subdomain
    domain = domain_info.domain

    features = {}

    # 1. UsoIP
    features["UsoIP"] = 1 if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", hostname) else 0

    # 2. URLLargo
    features["URLLargo"] = 1 if len(url) >= 54 else 0

    # 3. URLCorto
    features["URLCorto"] = 1 if len(url) <= 20 else 0

    # 4. SimboloArroba
    features["SimboloArroba"] = 1 if "@" in url else 0

    # 5. Redireccion
    features["Redireccion"] = 1 if url.count("//") > 1 else 0

    # 6. PrefijoSufijo
    features["PrefijoSufijo"] = 1 if "-" in domain else 0

    # 7. SubDominio
    features["SubDominio"] = 1 if subdomain and subdomain != "www" else 0

    # 8. HTTPS
    features["HTTPS"] = 1 if parsed.scheme == "https" else 0

    # 9. ExpiracionCreacionDominio
    features["ExpiracionCreacionDominio"] = 0

    # 10. Icono
    features["Icono"] = 0

    # 11. NoPuertoStd
    features["NoPuertoStd"] = 1 if parsed.port not in [None, 80, 443] else 0

    # 12. HTTPSURLDominio
    features["HTTPSURLDominio"] = features["HTTPS"]

    # 13. URLRespuesta
    features["URLRespuesta"] = 0

    # 14. URLAnclaje
    features["URLAnclaje"] = 1 if "#" in url else 0

    # 15. ScriptEnlaceEnEtiquetas
    features["ScriptEnlaceEnEtiquetas"] = 0

    # 16. ControladorFormulariosServidor
    features["ControladorFormulariosServidor"] = 0

    # 17. InformacionCorreo
    features["InformacionCorreo"] = 1 if "mail" in url else 0

    # 18. URLAnormal
    features["URLAnormal"] = 1 if "://" in url else 0

    # 19. ReenvioSitiosWeb
    features["ReenvioSitiosWeb"] = 1 if "//" in path else 0

    # 20. BarraEstadoPersonalizado
    features["BarraEstadoPersonalizado"] = 0

    # 21. DeshabilitacionClicDerecho
    features["DeshabilitacionClicDerecho"] = 0

    # 22. UsoVentanaEmergente
    features["UsoVentanaEmergente"] = 0

    # 23. RedireccionMarcoFlotante
    features["RedireccionMarcoFlotante"] = 0

    # 24. EdadDeDominio
    features["EdadDeDominio"] = 0

    # 25. GrabacionDNS
    features["GrabacionDNS"] = 0

    # 26. TraficoSitioWeb
    features["TraficoSitioWeb"] = 0

    # 27. RangoPagina
    features["RangoPagina"] = 0

    # 28. IndiceGoogle
    features["IndiceGoogle"] = 0

    # 29. EnlacesApuntanPagina
    features["EnlacesApuntanPagina"] = 1 if re.findall(r"http[s]?://", url) else 0

    # 30. ReporteEstadisticas
    features["ReporteEstadisticas"] = 0

    return features