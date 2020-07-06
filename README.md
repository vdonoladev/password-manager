# password-manager
Este script vai criar um banco de dados sqlite e vai criar e guardar suas senhas de forma encriptada.

Se alguém conseguir pegar sua base de dados e tentar ler vai ver entradas assim:

sqlite> SELECT * FROM KEYS;
d2a8116004294b7603acbea8fc372b9cdee3d7e9950d1efadd4fc0b0bb07eff4
43b05ba3a81c28de854d5f2ef8382535a7981f8cfd32654882c4b3232bef7e9f
1919b015f7a3563d194e01d3b06023a8de8fe94e6263f459df97dd303989bca0

Use para criar e guardar senhas diversas:

v = ver senha
c = criar senha
s = sair