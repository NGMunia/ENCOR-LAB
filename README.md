# ENCOR-LAB

BGP-Routing:

AS 123:
- Load-balancing:
  - Outbound traffic is via R1 (VRRPv3)
  - VRRP is configured with object tracking with the help
    of IPSLA
  - Inbound traffic is via R2 (AS-prepending)
  - AS is a non-transit AS
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
- LISP is running on top of MGRE (for privacy purposes)
- R6 acts as Map server/resolver
Cust-A
- IPsec VTI is configured between R7 and R8
- Multicast Traffic is propagated through the tunnel (PIM sparse mode) with static RP


Automation:
Company-X
- Automation is used to configure repetitive tasks on routers like SNMP etc.
- ive created basic APIs using FastAPI that combined with Netmiko to interact with network devices.
- Ive also created Jinja templates used in conjuction with Netmiko and FastAPi that are used to configure the routers.


Quality of Service:

Company-X LAN router:
  - Social media traffic is policed to 250kbps
  - Scavenger traffic (torrent) is dropped.
  - Traffic destined to R5 is marked as critical data and given a CBWFQ bandwidth of 30% of CIR

Security:

Company-X firewall
  - Zone based firewall is configured to separate LAN and Internet links