# leanix-cicd-examples

The examples in this repository help you to connect your CI/CD pipeline into LeanIX Microservice Intelligence. For all examples, please refer to https://dev.leanix.net/docs/authentication to learn about required authentication. 

The following examples are provided:


## Ansible
Uploads an example Ansible definition file into Microservice Intelligence - example can be fetched from https://docs.ansible.com/ansible/latest/collections/ansible/builtin/uri_module.html. It requires a three step execution:

* Upload the Integration API processor into your workspace, see `https://dev.leanix.net/docs/setup``
* Execute `python yaml2Ldif.py' to extract a valid ldif (be mindful to add your workspace id - see https://dev.leanix.net/docs/authentication#section-generate-api-tokens)
* Upload the LDIF via the Integration API


## Gradle Dependencies
Uploads example gradle dependencies into Microservice Intelligence. It requires a Microservice ID which is present as external ID in your workspace. The sample gradle dependency file can be extracted by calling

`gradle dependencies --configuration compileClasspath > dependencies.txt`

See also https://docs.gradle.org/current/userguide/viewing_debugging_dependencies.html#viewing-debugging-dependencies

## Maven Dependencies
Uploads example Maven dependencies into Microservice Intelligence. It requires a Microservice ID which is present as external ID in your workspace. The sample maven dependency file can be extracted by calling

`mvn org.codehaus.mojo:license-maven-plugin:download-licenses`

See also https://www.mojohaus.org/license-maven-plugin/download-licenses-mojo.html

## Metadata
Uploads an example metadata file into LeanIX Microservice Intelligence

## NPM Dependencies
Uploads example NPM dependencies into Microservice Intelligence. It requires a Microservice ID which is present as external ID in your workspace. The sample npm dependency file can be extracted by calling

`npm install license-checker --save`

See also https://www.npmjs.com/package/license-checker

## Swagger
Uploads example Swagger definition file into Microservice Intelligence to create API Fact Sheets. Example can be fetched from https://editor.swagger.io/. It requires a three step execution:

* Upload the Integration API processor into your workspace, see `https://dev.leanix.net/docs/setup``
* Execute `python yaml2Ldif.py' to extract a valid ldif (be mindful to add your workspace id - see https://dev.leanix.net/docs/authentication#section-generate-api-tokens)
* Upload the LDIF via the Integration API



