; filepath: c:\Users\Admin\Documents\web_debuggerIDE1\network_capture.asm
section .data
    AF_INET     equ 2
    SOCK_RAW    equ 3
    IPPROTO_TCP equ 6
    SHM_KEY     equ 0x1234
    BUF_SIZE    equ 65535

section .bss
    packet_buffer: resb BUF_SIZE
    shm_id:        resq 1
    socket_fd:     resd 1
;jokin this doesnt do anything
