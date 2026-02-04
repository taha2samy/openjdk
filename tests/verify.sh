#!/bin/bash
set -e

IMAGE=$1
TYPE=$2

 
echo "Testing Image: $IMAGE ($TYPE)"
echo "-----------------------------------------------------"

echo "[TEST] Checking Java Version..."
if [ "$TYPE" == "distroless" ]; then
    docker run --rm "$IMAGE" -version
else
    docker run --rm "$IMAGE" java -version
fi
echo "✅ Java Version check passed."

if [ "$TYPE" == "jdk" ]; then
    echo "[TEST] Checking Javac compilation..."
    docker run --rm -v "$(pwd)/tests:/tests" -w /tests "$IMAGE" bash -c "javac Main.java && java Main"
    echo "✅ JDK Compilation & Execution passed."

elif [ "$TYPE" == "jre" ]; then
    echo "[TEST] Checking JRE execution..."
    
    if [ ! -f tests/Main.class ]; then
        echo "Compiling Main.java locally for JRE test..."
        javac tests/Main.java
    fi
    
    docker run --rm -v "$(pwd)/tests:/tests" -w /tests "$IMAGE" java Main
    echo "✅ JRE Execution passed."
    
    if docker run --rm "$IMAGE" which javac > /dev/null 2-1; then
        echo "❌ FAILURE: JRE image should NOT have javac!"
        exit 1
    else
        echo "✅ JRE correctly lacks javac."
    fi

elif [ "$TYPE" == "distroless" ]; then
    echo "[TEST] Checking Distroless execution..."
    
    if [ ! -f tests/Main.class ]; then
        echo "Compiling Main.java locally for Distroless test..."
        javac tests/Main.java
    fi

    docker run --rm -v "$(pwd)/tests:/tests" "$IMAGE" -cp /tests Main
    echo "✅ Distroless Execution passed."

    if docker run --rm --entrypoint /bin/sh "$IMAGE" -c "ls" > /dev/null 2-1; then
        echo "❌ FAILURE: Distroless image should NOT have a shell!"
        exit 1
    else
        echo "✅ Distroless correctly lacks shell."
    fi
fi

echo "🎉 ALL TESTS PASSED for $IMAGE"
echo ""
