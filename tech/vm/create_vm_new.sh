#!/bin/bash

your_project = "bi-course-461012"
echo $your_project


gcloud compute instances create vm-ppltx-prod \
    --project=bi-course-461012 \
    --zone=us-central1-f \
    --machine-type=e2-medium \
    --network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY,subnet=default \
    --metadata=enable-osconfig=TRUE \
    --maintenance-policy=MIGRATE \
    --provisioning-model=STANDARD \
    --service-account=709644591291-compute@developer.gserviceaccount.com \
    --scopes=https://www.googleapis.com/auth/cloud-platform \
    --tags=http-server,https-server \
    --create-disk=auto-delete=yes,boot=yes,device-name=vm-ppltx-prod,image=projects/debian-cloud/global/images/debian-12-bookworm-v20250513,mode=rw,size=10,type=pd-balanced \
    --no-shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --labels=goog-ops-agent-policy=v2-x86-template-1-4-0,goog-ec-src=vm_add-gcloud \
    --reservation-affinity=any \
&& \
printf 'agentsRule:\n  packageState: installed\n  version: latest\ninstanceFilter:\n  inclusionLabels:\n  - labels:\n      goog-ops-agent-policy: v2-x86-template-1-4-0\n' > config.yaml \
&& \
gcloud compute instances ops-agents policies create goog-ops-agent-v2-x86-template-1-4-0-us-central1-f \
    --project=bi-course-461012 \
    --zone=us-central1-f \
    --file=config.yaml \
#&& \
#gcloud compute resource-policies create snapshot-schedule default-schedule-1 \
#    --project=bi-course-461012 \
#    --region=us-central1 \
#    --max-retention-days=14 \
#    --on-source-disk-delete=keep-auto-snapshots \
#    --daily-schedule \
#    --start-time=17:00 \
#&& \
#gcloud compute disks add-resource-policies vm-ppltx-prod \
#    --project=bi-course-461012 \
#    --zone=us-central1-f \
#    --resource-policies=projects/bi-course-461012/regions/us-central1/resourcePolicies/default-schedule-1