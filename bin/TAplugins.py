import sys, json, os, re, platform, itertools, importlib, TAvol

class amcache:
	mode="standard"

class apihooks:
	mode="standard"

class atoms:
	mode="standard"

class atomscan:
	mode="standard"

class auditpol:
	mode="standard"

class bigpools:
	mode="standard"

class bioskbd:
	mode="standard"

class cachedump:
	mode="standard"

class callbacks:
	mode="standard"

class clipboard:
	mode="standard"

class cmdline:
	mode="standard"

class cmdscan:
	mode="standard"

class connections:
	mode="standard"

class connscan:
	mode="standard"

class consoles:
	mode="standard"

class crashinfo:
	mode="standard"

class deskscan:
	mode="standard"

class devicetree:
	mode="standard"

class dlldump:
	mode="standard"

class dlllist:
	mode="standard"

class driverirp:
	mode="standard"

class drivermodule:
	mode="standard"

class driverscan:
	mode="standard"

class dumpcerts:
	mode="standard"

class dumpfiles:
	mode="standard"

class dumpregistry:
	mode="standard"

class editbox:
	mode="standard"

class envars:
	mode="standard"

class eventhooks:
	mode="standard"

class evtlogs:
	mode="standard"

class filescan:
	mode="standard"

class gahti:
	mode="standard"

class gditimers:
	mode="standard"

class gdt:
	mode="standard"

class getservicesids:
	mode="standard"

class getsids:
	mode="standard"

class handles:
	mode="standard"

class hashdump:
	mode="standard"

class hibinfo:
	mode="standard"

class hivedump:
	mode="standard"

class hivelist:
	mode="standard"

class hivescan:
	mode="standard"

class hpakextract:
	mode="standard"

class hpakinfo:
	mode="standard"

class idt:
	mode="standard"

class iehistory:
	mode="standard"

class imagecopy:
	mode="standard"

class imageinfo:
	mode="standard"

class impscan:
	mode="standard"

class joblinks:
	mode="standard"

class kdbgscan:
	mode="standard"

class kpcrscan:
	mode="standard"

class ldrmodules:
	mode="standard"

class limeinfo:
	mode="standard"

class linux_apihooks:
	mode="standard"

class linux_arp:
	mode="standard"

class linux_aslr_shift:
	mode="standard"

class linux_banner:
	mode="standard"

class linux_bash:
	mode="standard"

class linux_bash_env:
	mode="standard"

class linux_bash_hash:
	mode="standard"

class linux_check_afinfo:
	mode="standard"

class linux_check_creds:
	mode="standard"

class linux_check_evt_arm:
	mode="standard"

class linux_check_fop:
	mode="standard"

class linux_check_idt:
	mode="standard"

class linux_check_inline_kernel:
	mode="standard"

class linux_check_modules:
	mode="standard"

class linux_check_syscall:
	mode="standard"

class linux_check_syscall_arm:
	mode="standard"

class linux_check_tty:
	mode="standard"

class linux_cpuinfo:
	mode="standard"

class linux_dentry_cache:
	mode="standard"

class linux_dmesg:
	mode="standard"

class linux_dump_map:
	mode="standard"

class linux_dynamic_env:
	mode="standard"

class linux_elfs:
	mode="standard"

class linux_enumerate_files:
	mode="standard"

class linux_find_file:
	mode="standard"

class linux_getcwd:
	mode="standard"

class linux_hidden_modules:
	mode="standard"

class linux_ifconfig:
	mode="standard"

class linux_info_regs:
	mode="standard"

class linux_iomem:
	mode="standard"

class linux_kernel_opened_files:
	mode="standard"

class linux_keyboard_notifiers:
	mode="standard"

class linux_ldrmodules:
	mode="standard"

class linux_library_list:
	mode="standard"

class linux_librarydump:
	mode="standard"

class linux_list_raw:
	mode="standard"

class linux_lsmod:
	mode="standard"

class linux_lsof:
	mode="standard"

class linux_malfind:
	mode="standard"

class linux_memmap:
	mode="standard"

class linux_moddump:
	mode="standard"

class linux_mount:
	mode="standard"

class linux_mount_cache:
	mode="standard"

class linux_netfilter:
	mode="standard"

class linux_netscan:
	mode="standard"

class linux_netstat:
	mode="standard"

class linux_pidhashtable:
	mode="standard"

class linux_pkt_queues:
	mode="standard"

class linux_plthook:
	mode="standard"

class linux_proc_maps:
	mode="standard"

class linux_proc_maps_rb:
	mode="standard"

class linux_procdump:
	mode="standard"

class linux_process_hollow:
	mode="standard"

class linux_psaux:
	mode="standard"

class linux_psenv:
	mode="standard"

class linux_pslist:
	mode="standard"

class linux_pslist_cache:
	mode="standard"

class linux_psscan:
	mode="standard"

class linux_pstree:
	mode="standard"

class linux_psxview:
	mode="standard"

class linux_recover_filesystem:
	mode="standard"

class linux_route_cache:
	mode="standard"

class linux_sk_buff_cache:
	mode="standard"

class linux_slabinfo:
	mode="standard"

class linux_strings:
	mode="standard"

class linux_threads:
	mode="standard"

class linux_tmpfs:
	mode="standard"

class linux_truecrypt_passphrase:
	mode="standard"

class linux_vma_cache:
	mode="standard"

class linux_volshell:
	mode="standard"

class linux_yarascan:
	mode="standard"

class lsadump:
	mode="standard"

class mac_adium:
	mode="standard"

class mac_apihooks:
	mode="standard"

class mac_apihooks_kernel:
	mode="standard"

class mac_arp:
	mode="standard"

class mac_bash:
	mode="standard"

class mac_bash_env:
	mode="standard"

class mac_bash_hash:
	mode="standard"

class mac_calendar:
	mode="standard"

class mac_check_fop:
	mode="standard"

class mac_check_mig_table:
	mode="standard"

class mac_check_syscall_shadow:
	mode="standard"

class mac_check_syscalls:
	mode="standard"

class mac_check_sysctl:
	mode="standard"

class mac_check_trap_table:
	mode="standard"

class mac_compressed_swap:
	mode="standard"

class mac_contacts:
	mode="standard"

class mac_dead_procs:
	mode="standard"

class mac_dead_sockets:
	mode="standard"

class mac_dead_vnodes:
	mode="standard"

class mac_devfs:
	mode="standard"

class mac_dmesg:
	mode="standard"

class mac_dump_file:
	mode="standard"

class mac_dump_maps:
	mode="standard"

class mac_dyld_maps:
	mode="standard"

class mac_find_aslr_shift:
	mode="standard"

class mac_get_profile:
	mode="standard"

class mac_ifconfig:
	mode="standard"

class mac_interest_handlers:
	mode="standard"

class mac_ip_filters:
	mode="standard"

class mac_kernel_classes:
	mode="standard"

class mac_kevents:
	mode="standard"

class mac_keychaindump:
	mode="standard"

class mac_ldrmodules:
	mode="standard"

class mac_librarydump:
	mode="standard"

class mac_list_files:
	mode="standard"

class mac_list_kauth_listeners:
	mode="standard"

class mac_list_kauth_scopes:
	mode="standard"

class mac_list_raw:
	mode="standard"

class mac_list_sessions:
	mode="standard"

class mac_list_zones:
	mode="standard"

class mac_lsmod:
	mode="standard"

class mac_lsmod_iokit:
	mode="standard"

class mac_lsmod_kext_map:
	mode="standard"

class mac_lsof:
	mode="standard"

class mac_machine_info:
	mode="standard"

class mac_malfind:
	mode="standard"

class mac_memdump:
	mode="standard"

class mac_moddump:
	mode="standard"

class mac_mount:
	mode="standard"

class mac_netstat:
	mode="standard"

class mac_network_conns:
	mode="standard"

class mac_notesapp:
	mode="standard"

class mac_notifiers:
	mode="standard"

class mac_orphan_threads:
	mode="standard"

class mac_pgrp_hash_table:
	mode="standard"

class mac_pid_hash_table:
	mode="standard"

class mac_print_boot_cmdline:
	mode="standard"

class mac_proc_maps:
	mode="standard"

class mac_procdump:
	mode="standard"

class mac_psaux:
	mode="standard"

class mac_psenv:
	mode="standard"

class mac_pslist:
	mode="standard"

class mac_pstree:
	mode="standard"

class mac_psxview:
	mode="standard"

class mac_recover_filesystem:
	mode="standard"

class mac_route:
	mode="standard"

class mac_socket_filters:
	mode="standard"

class mac_strings:
	mode="standard"

class mac_tasks:
	mode="standard"

class mac_threads:
	mode="standard"

class mac_threads_simple:
	mode="standard"

class mac_timers:
	mode="standard"

class mac_trustedbsd:
	mode="standard"

class mac_version:
	mode="standard"

class mac_vfsevents:
	mode="standard"

class mac_volshell:
	mode="standard"

class mac_yarascan:
	mode="standard"

class machoinfo:
	mode="standard"

class malfind:
	mode="standard"

class mbrparser:
	mode="standard"

class memdump:
	mode="standard"

class memmap:
	mode="standard"

class messagehooks:
	mode="standard"

class mftparser:
	mode="standard"

class moddump:
	mode="standard"

class modscan:
	mode="standard"

class modules:
	mode="standard"

class multiscan:
	mode="standard"

class mutantscan:
	mode="standard"

class netscan:
	mode="standard"

class notepad:
	mode="standard"

class objtypescan:
	mode="standard"

class patcher:
	mode="standard"

class poolpeek:
	mode="standard"

class pooltracker:
	mode="standard"

class printkey:
	mode="standard"

class privs:
	mode="standard"

class procdump:
	mode="standard"

class pslist:
	mode="standard"

class psscan:
	mode="standard"

class pstree:
	mode="standard"

class psxview:
	mode="standard"

class qemuinfo:
	mode="standard"

class raw2dmp:
	mode="standard"

class screenshot:
	mode="standard"

class servicediff:
	mode="standard"

class sessions:
	mode="standard"

class shellbags:
	mode="standard"

class shimcache:
	mode="standard"

class shutdowntime:
	mode="standard"

class sockets:
	mode="standard"

class sockscan:
	mode="standard"

class ssdt:
	mode="standard"

class strings:
	mode="standard"

class svcscan:
	mode="standard"

class symlinkscan:
	mode="standard"

class thrdscan:
	mode="standard"

class threads:
	mode="standard"

class timeliner:
	mode="standard"

class timers:
	mode="standard"

class truecryptmaster:
	mode="standard"

class truecryptpassphrase:
	mode="standard"

class truecryptsummary:
	mode="standard"

class unloadedmodules:
	mode="standard"

class userassist:
	mode="standard"

class userhandles:
	mode="standard"

class vaddump:
	mode="standard"

class vadinfo:
	mode="standard"

class vadtree:
	mode="standard"

class vadwalk:
	mode="standard"

class vboxinfo:
	mode="standard"

class verinfo:
	mode="standard"

class vmwareinfo:
	mode="standard"

class volshell:
	mode="standard"

class win10cookie:
	mode="standard"

class windows:
	mode="standard"

class wintree:
	mode="standard"

class wndscan:
	mode="standard"

class yarascan:
	mode="standard"

