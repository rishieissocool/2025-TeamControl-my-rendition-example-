#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <arpa/inet.h>
#include <sys/mman.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/epoll.h>

#define PORT 9999
#define BUFFER_SIZE 8192
#define FLAG "[FLAG]"
#define SHARED_MEM "/udp_shared_mem"

void error_exit(const char *msg) {
    perror(msg);
    exit(EXIT_FAILURE);
}

int main() {
    int sockfd, epfd;
    struct sockaddr_in server_addr, client_addr;
    char buffer[BUFFER_SIZE];
    socklen_t addr_len = sizeof(client_addr);

    // Create shared memory
    int shm_fd = shm_open(SHARED_MEM, O_CREAT | O_RDWR, 0666);
    ftruncate(shm_fd, BUFFER_SIZE);
    char *shared_mem = mmap(NULL, BUFFER_SIZE, PROT_WRITE, MAP_SHARED, shm_fd, 0);
    
    // Create UDP socket
    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) error_exit("Socket creation failed");

    // Optimize for high-speed UDP
    int opt = 1;
    setsockopt(sockfd, SOL_SOCKET, SO_RCVBUF, &opt, sizeof(opt));
    setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
    setsockopt(sockfd, SOL_SOCKET, SO_ATTACH_REUSEPORT_CBPF, &opt, sizeof(opt)); // Load balancing

    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(PORT);

    if (bind(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) error_exit("Bind failed");

    // Use epoll for efficient I/O event handling
    epfd = epoll_create1(0);
    struct epoll_event ev, events[10];
    ev.events = EPOLLIN;
    ev.data.fd = sockfd;
    epoll_ctl(epfd, EPOLL_CTL_ADD, sockfd, &ev);

    printf("Listening on UDP %d...\n", PORT);

    while (1) {
        int nfds = epoll_wait(epfd, events, 10, -1);
        for (int i = 0; i < nfds; i++) {
            if (events[i].data.fd == sockfd) {
                int recv_len = recvfrom(sockfd, buffer, BUFFER_SIZE, 0, (struct sockaddr *)&client_addr, &addr_len);
                if (recv_len > 0) {
                    buffer[recv_len] = '\0';  // Null-terminate
                    if (strstr(buffer, FLAG) != NULL) {
                        strcpy(shared_mem, buffer);  // Store latest flagged message
                    }
                }
            }
        }
    }

    close(sockfd);
    return 0;
}