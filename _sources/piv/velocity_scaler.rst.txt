Class for scaling the velocity field
====================================

If during the piv process the interrogation or search window size or distance is decreased, the velocity field has to be scaled to the new :doc:`GridSpec <grid_spec>`.

.. autoclass:: piv.velocity_scaler.VelocityUpscaler

After the setup the scaling is done by an other function.

.. automethod:: piv.velocity_scaler.VelocityUpscaler.scale_field
