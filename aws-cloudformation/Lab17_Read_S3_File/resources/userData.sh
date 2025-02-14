 UserDataScript:
    Type: AWS::S3::Object
    Properties:
      Bucket: !Ref MyS3Bucket
      Key: "userdata.sh"
      ContentType: "text/x-shellscript"
      Content: |
        #!/bin/bash
        sudo yum update -y
        sudo yum install -y httpd php
        sudo systemctl start httpd
        sudo systemctl enable httpd
        echo "<?php phpinfo(); ?>" > /var/www/html/index.php
        systemctl is-active httpd > /tmp/apache_status.txt