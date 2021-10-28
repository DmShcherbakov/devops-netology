# devops-netology
first added line

.gitignore в корневом каталоге пустой, поэтому никаких исключений в себе не несет.
Файл terraform/.gitignore окажет влияниена сам каталог terraform и его подкаталоги:
**/.terraform/* - исключает из обработки все файлы в каталогах .terraform, расположенных на любом уровне вложенности относительно каталога terraform.
*.tfstate - исключает все файлы с расширением .tfstate в каталоге, где размещен .gitignore (в нашем случае, каталог terraform)
*.tfstate.* - исключает все файлы в каталоге terraform, в имени которых встречается .tfstate.
crash.log - исключает файл crash.log из каталога terraform
*.tfvars - исключает все файлы с расширением .tfvars в каталоге, где размещен .gitignore (в нашем случае, каталог terraform)
override.tf - исключает файл с указанным именем из каталога terraform
override.tf.json - исключает файл с указанным именем из каталога terraform
*_override.tf - исключает файлы из каталога terraform, где имя заканчивается на *_override.tf
*_override.tf.json - исключает файлы из каталога terraform, где имя заканчивается на *_override.tf.json
.terraformrc - исключает файл с указанным именем из каталога terraform
terraform.rc - исключает файл с указанным именем из каталога terraform
