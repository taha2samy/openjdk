#!/bin/bash
set -e

IMAGE=$1
TYPE=$2

COMPILER_IMAGE=$(echo "$IMAGE" | sed 's/jre-std/jdk-std/g' | sed 's/jre-distroless/jdk-std/g')

TEST_DIR="simple_test"

echo "-----------------------------------------------------"
echo "Testing Image: $IMAGE ($TYPE)"
echo "Using for compile: $COMPILER_IMAGE"
echo "-----------------------------------------------------"

sudo rm -f "$TEST_DIR"/*.class

echo "[TEST] Checking Java Version..."
if [ "$TYPE" == "distroless" ]; then
    docker run --rm "$IMAGE" -version
else
    docker run --rm "$IMAGE" java -version
fi
echo "✅ Java Version check passed."

echo "[TEST] Compiling Main.java using $COMPILER_IMAGE..."
docker run --rm -u root -v "$(pwd)/$TEST_DIR:/tests" -w /tests "$COMPILER_IMAGE" javac Main.java
sudo chown $(id -u):$(id -g) "$TEST_DIR"/Main.java || true
echo "✅ Compilation successful."

if [ "$TYPE" == "jdk" ] || [ "$TYPE" == "jre" ]; then
    echo "[TEST] Executing in Standard Image..."
    docker run --rm -v "$(pwd)/$TEST_DIR:/tests" -w /tests "$IMAGE" java Main
    echo "✅ Execution passed."
    
    if [ "$TYPE" == "jre" ]; then
        if docker run --rm "$IMAGE" java -version 2>&1 | grep -q "javac"; then
             echo "❌ FAILURE: JRE image should NOT have javac!"
             exit 1
        fi
    fi

elif [ "$TYPE" == "distroless" ]; then
    echo "[TEST] Executing in Distroless Image..."
    docker run --rm -v "$(pwd)/$TEST_DIR:/tests" "$IMAGE" -cp /tests Main
    echo "✅ Distroless Execution passed."
    
    if docker run --rm --entrypoint /bin/sh "$IMAGE" -c "ls" > /dev/null 2>&1; then
        echo "❌ FAILURE: Distroless image should NOT have a shell!"
        exit 1
    fi
fi

sudo rm -f "$TEST_DIR"/*.class
echo "🎉 ALL TESTS PASSED for $IMAGE"
echo ""
