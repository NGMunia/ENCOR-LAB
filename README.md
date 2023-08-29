# ENCOR-LAB

BGP-Routing:

AS 123:
- Load-balancing:
  - Outbound traffic is via R1 (VRRPv3)
  - VRRP is configured with object tracking with the help
    of IPSLA
  - Inbound traffic is via R2 (AS-prepending)
- AS is a non-transit AS

Private VLANs (UPDATE):
   - Private vlans have been configured on device (SW) to segregate traffic between clients
       - Community VLAN 100 - Company X
       - Isolated VLAN 101

AS-130
  - Removes the private-AS while advertising the 17.17.17.0/24 prefix
  - Advertises only a default-route to AS65530

AS-140
  - Advertises 140.140.140.0/24 as a summary prefix

AS-150
  - Advertises 150.150.150.0/24 as a summary prefix  

AS65530
  - Advertises 17.17.17.0/24 as a summary prefix


Overlay:

Company-X
  - DMVPN phase 2 tunnel between its HQ, Branch and R5 routers with HQ being the hub
  - OSPF is used to route traffic between tunnels
  - DMVPN MGRE tunnel is area 0 and HQ,R5 and Branch networks are Areas 10, 50, 20 respectively.

Company-A
  - LISP is used to advertise prefixes behind R16 and R26.
  - LISP is running on top of mGRE (for privacy purposes)
  - R6 acts as Map server/resolver

Cust-A
  - IPsec VTI is configured between R7 and R8
  - Multicast Traffic is propagated through the tunnel between R7 and R8(PIM sparse mode) with static RP


Automation:

Company-X
  - Automation is used to configure repetitive tasks on routers like SNMP etc.
  - ive created basic REST-APIs using FastAPI that combined with Netmiko to interact with network devices.
  - Ive also created Jinja templates used in conjuction with Netmiko and FastAPi that are used to configure the routers.


Quality of Service:

Company-X LAN router:
  - Social media traffic is policed to 250kbps
  - Scavenger traffic (torrent) is dropped.
  - Traffic destined to R5 is marked as critical data and given a CBWFQ bandwidth of 30% of CIR


NAT:

  - The router labeled as 'HTTP' operates in a manner that emulates the functionality of a web server.     
  - Port forwarding measures have been appropriately established on the router denoted as R4, thereby enabling the accessibility of the HTTP service through the following endpoint: http://44.67.28.4/.


Assurance:

Company-X
  - SNMP is configured on all Company-X routers to be monitored on the Server
  - NetFlow is configured on LAN router to monitor traffic type traversing the network


Security:

Company-X firewall
  - Zone based firewall is configured to separate LAN and Internet links
  - Control-plane policing has been configured on HQ, R5 and Branch routers


Images used:

  - Routers:  i86bi-linux-l3-adventerprisek9-ms.155-2.T.bin
  - Switches: i86bi_linux_l2-adventerprise-ms.high_iron_20170202.bin
  - Server:   Win2k16_14393.0.161119-1705.RS1_REFRESH_SERVER_EVAL_X64FRE_EN-US.ISO
  - Ubuntu:   Ubuntu Desktop VM
  - PCs:      Webterm docker