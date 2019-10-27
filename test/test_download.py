
from spainopendata import DownloadDataset

def main():
    urls = [
        # 'http://estadisticas.uclm.es/analytics/saw.dll?Download&Path=%2Fshared%2FEstad%C3%ADstica%20Institucional/Informes/Academico/PT%20-%20Matriculados&NQUser=inteligenciainstitucional&NQPassword=p7bFn0H6udk&ViewName=PorRama&Format=CSV&Extension=.csv&Action=Navigate',
        # 'https://datosabiertos.malaga.eu/recursos/ambiente/telec/201212.csv',
        # "https://datosabiertos.malaga.eu/recursos/urbanismoEInfraestructura/planimetria/callejero/da_cartografiaUnidadTrabajoSocial-25830.csv",
        # "http://apirtod.santfeliu.cat/api/datos/participacio_eleccions_europees_1994.csv?rnd=1066673342",
        # "https://abertos.xunta.gal/catalogo/economia-empresa-emprego/-/dataset/0194/afiliacions-seguridade-social-segundo-rexime/101/acceso-aos-datos.csv",
        # "https://abertos.xunta.gal/catalogo/economia-empresa-emprego/-/dataset/0405/rexistro-entidades-formacion-ambito-seguridade/101/acceso-aos-datos.ods",
        # "http://www.minetad.gob.es/es-ES/IndicadoresyEstadisticas/Documents/CuadroResumen.ods"
        "http://www.cis.es/cis/opencms/ES/formulario.jsp?dwld=/Microdatos/MD2626.zip"
    ]

    for url in urls:
        if DownloadDataset.is_downloadable(url):
            print("Downloadable")
            local_file = DownloadDataset.download(url)
            print(local_file)
        else:
            print("NOT Downloadable")

        print('-'*100)


if __name__ == "__main__":
    main()
