#include <stdlib.h>
#include <stdio.h>

#include <zip.h>
#include <unzip.h>
#ifdef _WIN32
    #include <iowin32.h>
#endif

/* TODO: create test for this headers */
#include <crypt.h>
#include <mztools.h>

int main(int argc, char** argv) {
    zipFile zfd = zipOpen("test_minizip_create.zip", APPEND_STATUS_CREATE);
    if (zfd == NULL) {
        printf("ZIP file create failed");
        exit(1);
    }
    
    int res = zipClose(zfd, "Test MiniZip create");
    if(res != 0) {
        printf("ZIP file close failed, res => %d", res);
        exit(1);
    }
    
    return 0;
}
