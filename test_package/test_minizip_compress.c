#include <stdlib.h>
#include <stdio.h>
#include <time.h>

#include <zip.h>
#include <unzip.h>
#ifdef _WIN32
    #include <iowin32.h>
#endif

/* TODO: create test for this headers */
#include <crypt.h>
#include <mztools.h>

#define SRC_SIZE 1024 * 1024
const char* zip_fname = "test_minizip_compress.zip";

void fill_data(char*, size_t);

int main(int argc, char** argv) {
    srand(time(0));

    zipFile zf = zipOpen(zip_fname, APPEND_STATUS_CREATE);
    if (zf == NULL) {
        printf("ZIP file create failed, fname => %s\n", zip_fname);
        exit(1);
    }
    
    char* data = malloc(SRC_SIZE);
    if (data == NULL) {
        printf("Can`t allocate source buffer\n");
        exit(1);
    }
    fill_data(data, SRC_SIZE);
    
    zip_fileinfo zfi = {0};
    int err = zipOpenNewFileInZip(zf, "fname.bin", &zfi, NULL, 0, NULL, 0, NULL, Z_DEFLATED, Z_DEFAULT_COMPRESSION);
    if (err != ZIP_OK) {
        printf("Open new file in ZIP failed\n");
        exit(1);
    }
    
    err = zipWriteInFileInZip(zf, data, SRC_SIZE);
    if (err != ZIP_OK) {
        printf("Write file in ZIP failed\n");
        exit(1);
    }
    
    err = zipCloseFileInZip(zf);
    if (err != ZIP_OK) {
        printf("Close file in ZIP failed\n");
        exit(1);
    }
        
    int res = zipClose(zf, "Test MiniZip create");
    if(res != 0) {
        printf("ZIP file close failed, res => %d\n", res);
        exit(1);
    }
    
    return 0;
}

void fill_data(char* data, size_t len) {
    for (size_t i = 0; i < len; i++) {
        *(data + i) = (char) rand();
    }
    return;
}
