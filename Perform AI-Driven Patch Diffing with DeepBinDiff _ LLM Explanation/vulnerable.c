#include <stdio.h>
#include <string.h>

void process_input(char *input) {
    char buffer[64];
    strcpy(buffer, input);  // Vulnerable: no bounds checking
    printf("Processed: %s\n", buffer);
}

int main(int argc, char *argv[]) {
    if (argc > 1) {
        process_input(argv[1]);
    }
    return 0;
}
EOF

# Create patched version
cat > patched.c << 'EOF'
#include <stdio.h>
#include <string.h>

void process_input(char *input) {
    char buffer[64];
    strncpy(buffer, input, sizeof(buffer)-1);  // Fixed: bounds checking
    buffer[sizeof(buffer)-1] = '\0';
    printf("Processed: %s\n", buffer);
}

int main(int argc, char *argv[]) {
    if (argc > 1) {
        process_input(argv[1]);
    }
    return 0;
}
