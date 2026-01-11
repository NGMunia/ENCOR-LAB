# ENCOR Enterprise Network Lab

**A full-scale enterprise and service-provider lab showcasing advanced routing, overlays, security, automation, QoS, and network assurance.**  
Designed to reflect enterprise network architectures aligned with **CCNP Enterprise (ENCOR)** objectives.
![Routing](https://img.shields.io/badge/BGP%20%7C%20OSPF-orange)
![DMVPN](https://img.shields.io/badge/DMVPN-Phase%202-green)
![Security](https://img.shields.io/badge/Cryptography-Ent-red)
![Automation](https://img.shields.io/badge/Automation-Python-orange)
![CCNP](https://img.shields.io/badge/CCNP-ENCOR-success)
![Quality of service](https://img.shields.io/badge/DiffServ-red)

---


![Topology](/Network-Topology.png)

## Quick Overview

- **Routing:** Multi-AS BGP, traffic engineering, summarization
- **Overlays:** DMVPN, LISP, IPsec VTI
- **Security:** Zone-Based Firewall, CoPP, segmentation, NAT
- **Automation:** Python, FastAPI, Netmiko, Jinja2
- **Monitoring:** SNMP, NetFlow
- **Level:** CCNP Enterprise (ENCOR)

---

## Project Objectives

- Design and implement multi-AS enterprise routing
- Apply BGP traffic engineering techniques
- Deploy scalable WAN overlay technologies
- Secure network infrastructure and control planes
- Automate repetitive network operations
- Monitor and analyze network performance and traffic flows

---

## Network Architecture

The lab simulates a hybrid **enterprise** environment with multiple autonomous systems, enterprise customers, and secure overlays.



---

## Routing & BGP Design

### AS 123 – Enterprise Edge

- Non-transit autonomous system
- Outbound traffic via **R1** using **VRRPv3**
- VRRP object tracking integrated with **IP SLA**
- Inbound traffic influenced via **AS-path prepending** toward **R2**
- Provides resiliency, redundancy, and deterministic traffic flow

```bash
track 1 ip sla 1
 delay down 5 up 5
!
!
interface Ethernet0/0
 ip address 44.67.28.1 255.255.255.0
 vrrp 1 address-family ipv4
  priority 110
  vrrpv2
  track 1 decrement 40
  address 44.67.28.3 primary
  exit-vrrp
!
!
ip sla 1
 icmp-echo 100.100.100.1 source-ip 100.100.100.2
 frequency 10
ip sla schedule 1 life forever start-time now

```

### Private VLANs

Implemented on the access switch to isolate customer traffic:

- **Community VLAN 100** – Company-X
- **Isolated VLAN 101**

Prevents lateral communication while maintaining shared infrastructure.

---

### BGP Autonomous Systems Overview

| AS Number | Function |
|---------|---------|
| AS 123 | Enterprise non-transit AS with traffic engineering |
| AS 130 | Removes private AS, advertises `17.17.17.0/24`, sends default route |
| AS 140 | Advertises summary prefix `140.140.140.0/24` |
| AS 150 | Advertises summary prefix `150.150.150.0/24` |
| AS 65530 | Upstream provider advertising summarized routes |

```bash
Non-transist-config (AS123):

router bgp 123
 bgp log-neighbor-changes
 network 44.67.28.0 mask 255.255.255.0
 neighbor 100.100.100.1 remote-as 100
 neighbor 100.100.100.1 route-map inbound-traffic-map out
 neighbor 100.100.100.1 filter-list 10 out
!
ip forward-protocol nd
!
ip as-path access-list 10 permit ^$

```
```bash
Removing-Private-AS
router bgp 130
 bgp log-neighbor-changes
 neighbor 2.2.2.2 remote-as 130
 neighbor 2.2.2.2 update-source Loopback0
 neighbor 2.2.2.2 next-hop-self
 neighbor 130.130.130.2 remote-as 100
 neighbor 130.130.130.2 remove-private-as
 neighbor 130.130.130.10 remote-as 150
 neighbor 130.130.130.10 remove-private-as
 ```
 ```bash
 AS-65530-Summary-prefix:
 !
router bgp 65530
 bgp log-neighbor-changes
 network 17.17.17.0 mask 255.255.255.252
 aggregate-address 17.17.17.0 255.255.255.0 summary-only
 neighbor 130.130.130.13 remote-as 130
 ```


## Overlay Technologies

### Company-X – DMVPN

- **DMVPN Phase 2**
- HQ acts as hub, Branch and R5 as spokes
- **OSPF** used as the overlay routing protocol (OSPF must be broadcast)
- Tunnel interface configured in **Area 0**
- Internal networks:
  - HQ – Area 10
  - Branch – Area 20
  - R5 – Area 50

```bash
crypto isakmp policy 100
 encr aes 192
 hash sha256
 authentication pre-share
 group 14
 lifetime 7200
crypto isakmp key strongkey address 0.0.0.0        
!
!
crypto ipsec transform-set crypt_ts esp-aes 192 esp-sha256-hmac 
 mode transport
!
crypto ipsec profile crypto-profile
 set transform-set crypt_ts 
!
!

interface Tunnel10
 ip address 172.19.10.1 255.255.255.0
 no ip redirects
 ip mtu 1400
 ip nhrp authentication xyzdmvpn
 ip nhrp map multicast dynamic
 ip nhrp network-id 10
 ip tcp adjust-mss 1360
 ip ospf network broadcast
 ip ospf hello-interval 15
 ip ospf 1 area 0
 tunnel source Ethernet0/0
 tunnel mode gre multipoint
 tunnel key 10
 tunnel protection ipsec profile crypto-profile
 ```

---

### Company-A – LISP

- **LISP** used to advertise prefixes behind R16 and R26
- Runs on top of **mGRE** for privacy
- **R6** acts as Map Server and Map Resolver
- Separates endpoint identity from location for scalability

---

### Cust-A – IPsec VTI

- **IPsec VTI** tunnel between R7 and R8
- Supports multicast traffic over VPN
- **PIM Sparse Mode** with a static Rendezvous Point (RP)

```bash
IPSEC-VTI
crypto isakmp policy 100
 encr aes
 hash sha256
 authentication pre-share
 group 5
 lifetime 7200
crypto isakmp key strongkey address 44.67.28.8
!
!
crypto ipsec transform-set crypt-ts esp-aes 192 esp-sha-hmac
 mode transport
!
crypto ipsec profile crypto-profile
 set transform-set crypt-ts
!

interface Tunnel78
 ip address 172.17.78.1 255.255.255.252
 ip pim sparse-mode
 tunnel source Ethernet0/0
 tunnel mode ipsec ipv4
 tunnel destination 44.67.28.8
 tunnel protection ipsec profile crypto-profile
 ```

---

## Automation & Programmability

### Company-X Automation

- Automated repetitive router configurations (e.g. SNMP)
- Integrated **Netmiko** for network device interaction

```python

from netmiko import ConnectHandler
from rich import print as rp
from Devices import Routers

for devices in Routers.values():
    conn = ConnectHandler(**devices)
    conn.enable()
    output = conn.send_command('show version',use_textfsm=True)
    rp(output)
```

---

## Quality of Service (QoS)

### Company-X LAN Router

- Social media traffic policed to **250 kbps**
- Scavenger traffic (torrent) dropped
- Traffic destined to **R5** marked as critical
- Critical traffic allocated **30% CBWFQ bandwidth** of CIR

```bash
QoS

class-map match-any Critical-traffic-class
 match access-group name critical-traffic-acl
class-map match-any Social-media-class
 match protocol twitter
 match protocol facebook
 match protocol instagram
class-map match-any Scavenger-traffic-class
 match protocol bittorrent
 match protocol netflix
!
policy-map Network-traffic-policy
 class Scavenger-traffic-class
  drop
 class Social-media-class
  set dscp af13
  police 250000 conform-action transmit  exceed-action drop 
 class Critical-traffic-class
  bandwidth percent 30 
  set dscp af31
!
!
interface Ethernet0/0
 ip address 192.168.10.1 255.255.255.0
 ip nbar protocol-discovery
 ip flow ingress
 ip flow egress
 ip ospf 1 area 10
!
interface Ethernet0/1
 ip address 10.0.0.2 255.255.255.252
 ip ospf network point-to-point
 ip ospf 1 area 10
 service-policy output Network-traffic-policy
```


---

## Network Address Translation (NAT)

- Router labeled **HTTP** emulates a web server
- Port forwarding configured on **R4**
- HTTP service accessible via:

```text
http://44.67.28.4/

```
```bash
ip nat inside source static tcp 192.168.40.100 80 44.67.28.4 80 extendable
```

---

##  Network Assurance

### Company-X
 - SNMP is configured on all Company-X routers to be monitored on the Server
 - NetFlow is configured on LAN, R5 and Branch-1 routers to monitor traffic type traversing  from the LAN network

 ```bash

ip access-list standard snmp_acl
 permit 192.168.50.100
!
snmp-server community device_snmp RO snmp_acl
snmp-server system-shutdown
snmp-server enable traps config
snmp-server host 192.168.50.100 version 2c device_snmp 
```
```bash
COPP

ip access-list extended Icmp-CoPP-acl
 permit icmp any any
ip access-list extended Management-CoPP-acl
 permit udp host 192.168.50.100 any eq snmp
 permit tcp any any eq 22
ip access-list extended Routing-CoPP-acl
 permit ospf any host 224.0.0.6
!
!
control-plane
 service-policy input CoPP-Policy
 ```


---
## Security:

Company-X firewall
  - Zone based firewall is configured to separate LAN and Internet links
  - Control-plane policing has been configured on HQ, R5 and Branch routers
  
```bash
class-map type inspect match-any inside-internet-class
 match protocol tcp
 match protocol udp
 match protocol icmp
!
policy-map type inspect inside-internet-policy
 class type inspect inside-internet-class
  inspect 
 class class-default
  drop
!
zone security Inside
zone security Internet
zone-pair security inside-internet-zone source Inside destination Internet
 service-policy type inspect inside-internet-policy
! 

interface Ethernet0/0
 ip address 10.0.0.1 255.255.255.252
 ip nat inside
 ip virtual-reassembly in
 zone-member security Inside
 ip ospf network point-to-point
 ip ospf 1 area 10
!
interface Ethernet0/1
 ip address 10.0.0.5 255.255.255.252
 zone-member security Inside
 ip ospf network point-to-point
 ip ospf 1 area 10
 ```


## Images used:

  - Routers:  i86bi-linux-l3-adventerprisek9-ms.155-2.T.bin
  - Switches: i86bi_linux_l2-adventerprise-ms.high_iron_20170202.bin
  - Server:   Win2k16_14393.0.161119-1705.RS1_REFRESH_SERVER_EVAL_X64FRE_EN-US.ISO
  - Ubuntu:   Ubuntu Desktop VM
  - PCs:      Webterm docker


