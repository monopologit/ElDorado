import React from "react";

const GuiaUsuario = () => {
  return (
    <div className="w-full max-w-3xl mx-auto bg-white rounded-2xl p-6 my-8 border border-cyan-200 shadow">
      <h2 className="text-2xl font-extrabold text-orange-600 mb-4 tracking-wider uppercase text-center">
        Guía de Usuario
      </h2>
      <article className="prose prose-sm max-w-none" style={{fontSize: '1.1em'}}>
        <p>
          <b>Bienvenido al sistema de trazabilidad de vagonetas y ladrillos</b>.<br/>
          Esta plataforma fue desarrollada para modernizar y optimizar el control de producción en la fábrica de ladrillos, utilizando visión computacional y tecnologías de inteligencia artificial. El sistema automatiza la identificación de vagonetas y el registro de su carga, permitiendo un seguimiento preciso y seguro de cada movimiento dentro del proceso de secado.
        </p>
        <p>
          <b>¿Cómo funciona el sistema?</b><br/>
          El sistema analiza imágenes o videos capturados en los puntos de control del secadero. Detecta automáticamente las vagonetas, reconoce el número de chapa mediante OCR y clasifica el tipo de ladrillo transportado. Toda la información relevante (número, modelo, fecha, hora, túnel, evento, merma) se almacena en una base de datos centralizada, permitiendo su consulta y análisis posterior.
        </p>
        <p>
          <b>¿Qué puedes hacer desde la web?</b>
        </p>
        <ul className="list-disc ml-6">
          <li><b>Subir imágenes o videos:</b> Desde la sección "Subir Imagen" o "Subir Video", puedes cargar archivos capturados por cámaras de control. El sistema procesará automáticamente el contenido y te informará si la detección fue exitosa, mostrando el número de vagoneta y el modelo de ladrillo identificados.</li>
          <li><b>Capturar en tiempo real:</b> Si tienes una cámara conectada, puedes usar la opción "Cámara Tiempo Real" para tomar una foto al instante y procesarla en el sistema.</li>
          <li><b>Consultar historial:</b> Accede a la sección "Ver Historial" para revisar todos los movimientos registrados. Puedes filtrar por número de vagoneta, fecha, túnel, modelo de ladrillo, evento o merma para encontrar información específica.</li>
          <li><b>Ver trayectoria:</b> En la sección "Trayectoria", ingresa el número de una vagoneta para visualizar todos sus movimientos, condiciones de secado y estadísticas asociadas, facilitando el análisis de la producción y la calidad.</li>
        </ul>
        <p>
          <b>Ventajas y recomendaciones de uso:</b><br/>
          - <b>Automatización:</b> Elimina el registro manual y reduce errores humanos.<br/>
          - <b>Control total:</b> Permite reconstruir la historia de cada vagoneta y su carga, asociando datos de temperatura y humedad para optimizar el proceso.<br/>
          - <b>Facilidad de uso:</b> La interfaz es intuitiva y no requiere conocimientos técnicos. Sigue los mensajes y avisos en pantalla para cada acción.<br/>
          - <b>Accesibilidad:</b> Puedes acceder al sistema desde cualquier computadora conectada a la red interna de la fábrica.
        </p>
        <p>
          <b>Ejemplo de flujo de trabajo:</b><br/>
          1. Un operario sube una imagen de una vagoneta ingresando al secadero.<br/>
          2. El sistema detecta la vagoneta, extrae el número de chapa y clasifica el modelo de ladrillo.<br/>
          3. El registro se almacena automáticamente en la base de datos.<br/>
          4. Más tarde, otro usuario puede consultar el historial o la trayectoria de esa vagoneta, verificando las condiciones de secado y la calidad del proceso.<br/>
        </p>
        <p>
          <b>Contexto general:</b><br/>
          Este sistema es parte de una iniciativa para digitalizar y optimizar la producción de ladrillos, facilitando la toma de decisiones, la trazabilidad y la mejora continua en la fábrica.
        </p>
      </article>
    </div>
  );
};

export default GuiaUsuario;
