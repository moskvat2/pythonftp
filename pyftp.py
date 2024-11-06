import ftplib
import os

FILESIZE=0 # qualquer arquivo maior que zero, medida em bytes

def download_arquivos_bak_com_subpastas_e_filtro(host, user, password, remote_dir, local_dir, tamanho_minimo=FILESIZE * 1024 * 1024 * 1024):
  try:
    with ftplib.FTP(host) as ftp:
      ftp.login(user, password)
      ftp.cwd(remote_dir)

      def download_pasta(remote_path, local_path):
        ftp.cwd(remote_path)
        filenames = ftp.nlst()
        for filename in filenames:
          remote_file = os.path.join(remote_path, filename)
          local_file = os.path.join(local_path, filename)

          if filename.endswith('.png'):
            # Verifica o tamanho do arquivo
            size = ftp.size(filename)
            if size >= tamanho_minimo:
              with open(local_file, 'wb') as f:
                ftp.retrbinary('RETR ' + filename, f.write)
              print(f"Arquivo {remote_file} (tamanho: {size} bytes) baixado para {local_file}")
            else:
              print(f"Arquivo {remote_file} (tamanho: {size} bytes) ignorado (menor que o tamanho mínimo)")
          else:
            if not os.path.exists(local_file):
              os.makedirs(local_file)
            download_pasta(remote_file, local_file)

      download_pasta(remote_dir, local_dir)

  except ftplib.all_errors as e:
    print(f"Erro ao baixar os arquivos: {e}")

# Exemplo de uso:
host = "localhost"
user = "teste"
password = "teste"
remote_dir = "/"
local_dir = "downloads"

download_arquivos_bak_com_subpastas_e_filtro(host, user, password, remote_dir, local_dir)
