mkdir package

python3 -m pip install \
  --platform manylinux2014_x86_64 \
  --implementation cp \
  --python-version 3.12 \
  --abi cp312 \
  --only-binary=:all: \
  --target package \
  Pillow

cp lambda_function.py package/

cd package
zip -r ../lambda-function.zip .
cd ..