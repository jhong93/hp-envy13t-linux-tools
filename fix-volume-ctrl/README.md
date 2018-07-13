# Fix the volume control on HP Envy 13t

Use hda-jack-retask to enable pin 0x14 and set a boot override. This enables
sound on all four speakers, but no volume control on two of the speakers. This
script configures volume control on all four speakers and runs as a daemon
managed by systemd.
