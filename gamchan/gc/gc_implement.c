#include <stdio.h>
#include <stdlib.h>

typedef struct MemoryBlock {
    void* address;
    size_t size;
    struct MemoryBlock* next;
} MemoryBlock;

MemoryBlock* head = NULL;

void* custom_malloc(size_t size) {
    void* result = malloc(size);
    if (result) {
        MemoryBlock* newBlock = (MemoryBlock*)malloc(sizeof(MemoryBlock));
        newBlock->address = result;
        newBlock->size = size;
        newBlock->next = head;
        head = newBlock;
    }
    return result;
}

void custom_free(void* ptr) {
    MemoryBlock* current = head;
    MemoryBlock* prev = NULL;

    while (current != NULL) {
        if (current->address == ptr) {
            if (prev) {
                prev->next = current->next;
            } else {
                head = current->next;
            }
            free(current);
            break;
        }
        prev = current;
        current = current->next;
    }
    free(ptr);
}

void printAllocations() {
    MemoryBlock* current = head;
    while (current) {
        printf("Address: %p, Size: %zu\n", current->address, current->size);
        current = current->next;
    }
}

int main() {
    char* data1 = (char*)custom_malloc(10);
    int* data2 = (int*)custom_malloc(sizeof(int) * 5);

    printAllocations();

    custom_free(data1);
    custom_free(data2);

    return 0;
}