import numpy as np

class VectorMath:
    @staticmethod
    def calculate_angle(a, b, c):
        """Calculates the angle between three points (in degrees)."""
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        
        if angle > 180.0:
            angle = 360 - angle
            
        return angle

    @staticmethod
    def get_vector_angle(v1, v2):
        """Calculates the angle between two vectors."""
        unit_v1 = v1 / np.linalg.norm(v1)
        unit_v2 = v2 / np.linalg.norm(v2)
        dot_product = np.dot(unit_v1, unit_v2)
        angle = np.arccos(np.clip(dot_product, -1.0, 1.0))
        return np.degrees(angle)

    @staticmethod
    def get_bone_rotation(joint_pos, parent_pos, child_pos):
        """
        Calculates the rotation offset for a bone in 3D space.
        Returns a rotation matrix representing the bone's orientation.
        """
        # Vector from joint to child (the bone direction)
        bone_vec = child_pos - joint_pos
        bone_vec /= np.linalg.norm(bone_vec)
        
        # Reference vector (e.g., world up or parent forward)
        ref_vec = np.array([0, 1, 0])
        
        # Calculate rotation to align ref_vec to bone_vec
        return VectorMath.get_rotation_matrix(ref_vec, bone_vec)

    @staticmethod
    def calculate_relative_angle(p1, p2, p3):
        """Calculates internal angle between three 3D points."""
        v1 = p1 - p2
        v2 = p3 - p2
        
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        
        if norm1 == 0 or norm2 == 0:
            return 0
            
        dot = np.dot(v1, v2)
        angle = np.arccos(np.clip(dot / (norm1 * norm2), -1.0, 1.0))
        return np.degrees(angle)
